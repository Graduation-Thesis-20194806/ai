import boto3
from os import getenv

AWS_REGION = getenv("AWS_REGION")
AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = getenv("AWS_SECRET_ACCESS_KEY")


if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
    s3_client = boto3.client("s3",
                                region_name=AWS_REGION,
                                aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    sqs = boto3.client('sqs', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                       region_name=AWS_REGION)
else:
    s3_client = boto3.client("s3", region_name=AWS_REGION)
    sqs = boto3.client('sqs',region_name=AWS_REGION)


def send_message(message_body: str, message_group_id: str, delay_seconds: int = 0):
    response = sqs.send_message(
        QueueUrl="https://sqs.ap-southeast-1.amazonaws.com/680828732035/ThesisQueue.fifo",
        MessageBody=message_body,
        DelaySeconds=delay_seconds,
        MessageGroupId=message_group_id
    )
    print(f"Message sent. MessageId: {response.get('MessageId')}")