import requests
import google.generativeai as genai
import config

# Use the API keys from config.py
github_key = config.GITHUB_KEY
gemini_key = config.GEMINI_KEY

import requests

def fetch_all_issues_and_prs(token, owner, repo_name):
    url = 'https://api.github.com/graphql'
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

    # GraphQL query template to fetch both issues and PRs
    query_template = """
    query ($owner: String!, $repoName: String!, $count: Int!, $issuesCursor: String, $prsCursor: String) {
      repository(owner: $owner, name: $repoName) {
        issues(first: $count, after: $issuesCursor) {
          edges {
            node {
              title
              url
              createdAt
              number
            }
            cursor
          }
          pageInfo {
            endCursor
            hasNextPage
          }
        }
        pullRequests(first: $count, after: $prsCursor) {
          edges {
            node {
              title
              url
              createdAt
              number
            }
            cursor
          }
          pageInfo {
            endCursor
            hasNextPage
          }
        }
      }
    }
    """

    all_issues = []
    all_prs = []
    issues_cursor = None
    prs_cursor = None

    while True:
        variables = {'owner': owner, 'repoName': repo_name, 'count': 100, 'issuesCursor': issues_cursor, 'prsCursor': prs_cursor}

        response = requests.post(url, json={'query': query_template, 'variables': variables}, headers=headers)
        if response.status_code == 200:
            data = response.json()

            # Process issues
            issues = data['data']['repository']['issues']['edges']
            all_issues.extend(issues)
            if data['data']['repository']['issues']['pageInfo']['hasNextPage']:
                issues_cursor = data['data']['repository']['issues']['pageInfo']['endCursor']
            else:
                issues_cursor = None

            # Process PRs
            prs = data['data']['repository']['pullRequests']['edges']
            all_prs.extend(prs)
            if data['data']['repository']['pullRequests']['pageInfo']['hasNextPage']:
                prs_cursor = data['data']['repository']['pullRequests']['pageInfo']['endCursor']
            else:
                prs_cursor = None

            if issues_cursor is None and prs_cursor is None:
                # No more pages for both issues and PRs
                break
        else:
            print(f"Query failed to run with a {response.status_code}")
            break

    return all_issues, all_prs


repo_url = input("Enter the Github Repo URL: ")

# Extract repo owner and name from the URL
owner, repo_name = repo_url.split('/')[-2:]

# Fetch merged PRs
merged_prs = fetch_all_issues_and_prs(github_key, owner, repo_name)


