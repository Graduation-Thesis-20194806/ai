import json
import os
import shutil
import zipfile
from os import getenv

import redis
from botocore.exceptions import NoCredentialsError
from celery import Celery

from .aws import s3_client, send_message
from .constant import MessageType, DuplicateLevel
from .issue_type_process import issue_type_process
from .llm_api import chat
from ..models import BugReport, ReportIssueType
from ..models.database import SessionLocal
from ..repositories import BugReportRepository
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine

redis_url = f"redis://{getenv("REDIS_HOST")}:{getenv("REDIS_PORT")}/0"
celery = Celery(__name__, broker=redis_url, backend=redis_url, broker_connection_retry_on_startup=True)
redis_client = redis.StrictRedis(host=getenv('REDIS_HOST'), port=int(getenv('REDIS_PORT')), db=0)


@celery.task
def process_report(report_id: int):
    db = SessionLocal()
    bugreport_repository = BugReportRepository(db, BugReport)
    report = bugreport_repository.find_by_id(report_id)

    if not report:
        return f"Report {report_id} not found"

    result = issue_type_process(report)
    issue_type = None
    for i in [
        ReportIssueType.UI,
        ReportIssueType.FUNCTIONAL,
        ReportIssueType.PERFORMANCE,
        ReportIssueType.SECURITY,
        ReportIssueType.NETWORK,
        ReportIssueType.DATA,
        ReportIssueType.OTHER,
    ]:
        if i.value in result:
            issue_type = i
            break

    send_message(json.dumps(
        {"type": MessageType.BUG_REPORT.value, "reportId": report_id, "issueType": issue_type.value}), MessageType.BUG_REPORT.value)
    return f"Report {report_id} processed successfully"


@celery.task
def process_duplicate(report_id: int):
    db = SessionLocal()
    bugreport_repository = BugReportRepository(db, BugReport)
    report = bugreport_repository.find_by_id(report_id)
    if not report:
        return f"Report {report_id} not found"
    reports = bugreport_repository.find_similar_reports(report)
    if len(reports) == 0:
        return f"No Report similar to {report_id}"
    return_data = {"type": MessageType.BUG_DUPLICATE.value, "reportId": report_id}
    for compare_report in reports:
        similarity = check_dup_report(report, compare_report)
        print(compare_report.id, similarity)
        dup_report_ids = []
        if similarity >= 0.5:
            if similarity < 0.7:
                level = DuplicateLevel.LOW.value
            elif similarity < 0.9:
                level = DuplicateLevel.MEDIUM.value
            else:
                level = DuplicateLevel.HIGH.value
            dup_report_ids.append({"id": compare_report.id, "level": level})
        return_data["dupReportIds"] = dup_report_ids
        return_data["type"] = MessageType.BUG_DUPLICATE.value
    send_message(json.dumps(return_data), MessageType.BUG_DUPLICATE.value)
    return f"Report {report_id} duplicate processed successfully"


def encode_description(description: str, model):
    return model.encode(description)


def check_similarity(description1: str, description2: str, model):
    vector1 = encode_description(description1, model)
    vector2 = encode_description(description2, model)
    similarity = 1 - cosine(vector1, vector2)
    return similarity


def check_dup_report(report1: BugReport, report2: BugReport):
    model = SentenceTransformer('bert-base-nli-mean-tokens')
    similarity = []
    fields = ['steps_to_reproduce']
    sum = 0
    for field in fields:
        if not report1.__getattribute__(field) or not report2.__getattribute__(field):
            continue
        similarity_score = check_similarity(report1.__getattribute__(field), report2.__getattribute__(field), model)
        similarity.append(similarity_score)
        sum += similarity_score

    description_similarity = check_similarity(report1.description, report2.description, model)

    if not len(similarity):
        return description_similarity
    final_score = (float(sum / len(similarity)) + description_similarity * 2) / 3
    return final_score

@celery.task
def download_model():
    inspect = celery.control.inspect()
    active_tasks = inspect.active()
    count = 0
    if active_tasks:
        for worker, tasks in active_tasks.items():
            for task in tasks:
                if task['name'] == 'app.utils.queue.download_model':
                    count += 1
                    if count >= 2:
                        return f"Exist running Task app.utils.queue.download_model"
    MODEL_FILE_NAME = 'paraphrase-multilingual-MiniLM-L12-v2'
    MODEL_FOLDER = os.sep.join(["model", "rough_match_model"])
    LOCAL_MODEL_PATH = os.sep.join([MODEL_FOLDER, MODEL_FILE_NAME])
    ZIP_MODEL_PATH = f"{LOCAL_MODEL_PATH}.zip"

    if not os.path.exists(LOCAL_MODEL_PATH):
        if os.path.exists(MODEL_FOLDER):
            shutil.rmtree(MODEL_FOLDER)
            print(f"Folder '{MODEL_FOLDER}' has been deleted.")
        parts = MODEL_FOLDER.split(os.sep)
        current_path = None
        for part in parts:
            current_path = os.sep.join([current_path, part]) if current_path else part
            if not os.path.exists(current_path):
                os.makedirs(current_path)
                print(f"Created folder: {current_path}")
            else:
                print(f"Folder already exists: {current_path}")
        try:
            s3_client.download_file(Bucket=os.getenv("S3_BUCKET_NAME"), Key=getenv('MODEL_S3_KEY'),
                                    Filename=ZIP_MODEL_PATH)
            extract_to = os.path.dirname(ZIP_MODEL_PATH)
            with zipfile.ZipFile(ZIP_MODEL_PATH, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            os.remove(ZIP_MODEL_PATH)
            print("Model downloaded successfully.")
        except NoCredentialsError:
            print("Credentials not available for AWS S3.")
        except Exception as e:
            print(f"An error occurred: {e}")