import csv
import os

import requests
import json
import concurrent.futures
import time
from dotenv import load_dotenv
from os import getenv

load_dotenv()
GITHUB_TOKEN = getenv('GITHUB_TOKEN')
HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"token {GITHUB_TOKEN}"
}

REPOS = [
    {
        'owner': 'magento',
        'repo': 'magento2',
        'labels': ['bug report'],
        'max_pages': 1000,
    },
    {
        'owner': 'woocommerce',
        'repo': 'woocommerce',
        'labels': ['type: bug'],
        'max_pages': 1000,
    },
    {
        'owner': 'PrestaShop',
        'repo': 'PrestaShop',
        'labels': ['Bug'],
        'max_pages': 1000,
    }
]

MAX_WORKERS = 3

def get_issues_of_repo(info: dict):
    owner = info['owner']
    repo = info['repo']
    labels = info['labels']
    max_pages = info['max_pages']
    start_page = info['start_page'] if 'start_page' in info else 1
    count = 0
    file_path = os.path.join('crawler', 'result',f"{owner}_{repo}.csv")
    file_exists = os.path.exists(file_path)
    headers = ["id", "owner","repo","number","title","body","state","created_at","updated_at","closed_at"]
    if not file_exists:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()

    for page in range(start_page, max_pages + 1):
        page_data = []
        url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        params = {
            "page": page,
            "state": "all",
            "labels": ",".join(labels),
        }
        resp = requests.get(url, headers=HEADERS, params=params)
        if resp.status_code == 200:
            print(f"{owner}/{repo}/{page}")
            issues = resp.json()
            if not issues:
                break
            for issue in issues:
                page_data.append({
                    "id": issue["id"],
                    "owner": owner,
                    "repo": repo,
                    "number": issue["number"],
                    "title": issue["title"],
                    "body": issue["body"],
                    "created_at": issue["created_at"],
                    "updated_at": issue["updated_at"] if "updated_at" in issue else None,
                    "closed_at": issue["closed_at"]  if "closed_at" in issue else None,
                    "state": issue["state"],

                })
            with open(file_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=headers)

                writer.writerows(page_data)
            count+=len(page_data)
        else:
            print(f"[*] Error while fetching issues from {owner}/{repo} (status code: {resp.status_code})")
            break

    return count

def crawl_repos(repo_list):
    results = {}

    # Use ThreadPoolExecutor for multi-threading
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Create a mapping from Future -> repo name
        future_to_repo = {
            executor.submit(get_issues_of_repo, repo): f"{repo['owner']}/{repo['repo']}"
            for repo in repo_list
        }

        # Collect results as each future completes
        for future in concurrent.futures.as_completed(future_to_repo):
            repo = future_to_repo[future]
            # try:
            data = future.result()
            results[repo] = data
            print(f"[+] Finished crawling {repo}, number of issues: {data}")
            # except Exception as exc:
            #     print(f"[!] Error while crawling {repo}: {exc}")

    return results

if __name__ == "__main__":
    start_time = time.time()

    os.makedirs(os.path.join('crawler','result'), exist_ok=True)

    # Crawl issues
    all_crawled_data = crawl_repos(REPOS)

    # Print total number of issues
    total_issues = sum(total for total in all_crawled_data.values())
    print(f"\nTotal issues crawled: {total_issues}")

    print(f"Execution time: {time.time() - start_time:.2f} seconds")