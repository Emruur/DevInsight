import requests
import json
import time
import base64

# Replace these with your own GitHub token and username
GITHUB_TOKEN = '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'
USERNAME = 'Emruur'
REPO_NAME = 'dummy-repo'
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

# Function to create a repository
def create_repository():
    url = f'https://api.github.com/user/repos'
    payload = {
        'name': REPO_NAME,
        'private': False
    }
    response = requests.post(url, headers=HEADERS, data=json.dumps(payload))
    if response.status_code == 201:
        print(f'Repository {REPO_NAME} created successfully')
    else:
        print(f'Failed to create repository: {response.json()}')
    return response.json()

# Function to create an issue
def create_issue(issue_title, issue_body, assignees):
    url = f'https://api.github.com/repos/{USERNAME}/{REPO_NAME}/issues'
    payload = {
        'title': issue_title,
        'body': issue_body,
        'assignees': assignees
    }
    response = requests.post(url, headers=HEADERS, data=json.dumps(payload))
    if response.status_code == 201:
        print(f'Issue "{issue_title}" created successfully')
        return response.json()  # Return the issue details if created successfully
    else:
        print(f'Failed to create issue: {response.json()}')
        return None  # Return None if issue creation failed

# Function to comment on an issue
def comment_issue(issue_number, comment):
    url = f'https://api.github.com/repos/{USERNAME}/{REPO_NAME}/issues/{issue_number}/comments'
    payload = {
        'body': comment
    }
    response = requests.post(url, headers=HEADERS, data=json.dumps(payload))
    if response.status_code == 201:
        print(f'Comment on issue #{issue_number} added successfully')
    else:
        print(f'Failed to add comment on issue: {response.json()}')

# Function to close an issue
def close_issue(issue_number):
    url = f'https://api.github.com/repos/{USERNAME}/{REPO_NAME}/issues/{issue_number}'
    payload = {
        'state': 'closed'
    }
    response = requests.patch(url, headers=HEADERS, data=json.dumps(payload))
    if response.status_code == 200:
        print(f'Issue #{issue_number} closed successfully')
    else:
        print(f'Failed to close issue: {response.json()}')

# Function to create a commit
def create_commit(file_path, message, content, branch='main'):
    url = f'https://api.github.com/repos/{USERNAME}/{REPO_NAME}/contents/{file_path}'
    payload = {
        'message': message,
        'content': base64.b64encode(content.encode('utf-8')).decode('ascii'),
        'branch': branch
    }
    response = requests.put(url, headers=HEADERS, data=json.dumps(payload))
    if response.status_code == 201:
        print(f'Commit "{message}" created successfully on branch "{branch}"')
    else:
        print(f'Failed to create commit: {response.json()}')
    return response.json()

# Function to create a pull request
def create_pull_request(head_branch, base_branch='main', issue_number=None):
    url = f'https://api.github.com/repos/{USERNAME}/{REPO_NAME}/pulls'
    body = 'This is a dummy pull request'
    if issue_number:
        body += f'\n\nFixes #{issue_number}'
    payload = {
        'title': f'PR from {head_branch} to {base_branch}',
        'head': head_branch,
        'base': base_branch,
        'body': body
    }
    response = requests.post(url, headers=HEADERS, data=json.dumps(payload))
    if response.status_code == 201:
        print(f'Pull request from {head_branch} to {base_branch} created successfully')
        return response.json()  # Return the pull request details if created successfully
    else:
        print(f'Failed to create pull request: {response.json()}')
        return None  # Return None if pull request creation failed

# Function to merge a pull request
def merge_pull_request(pr_number):
    url = f'https://api.github.com/repos/{USERNAME}/{REPO_NAME}/pulls/{pr_number}/merge'
    payload = {
        'commit_message': 'Merging pull request'
    }
    response = requests.put(url, headers=HEADERS, data=json.dumps(payload))
    if response.status_code == 200:
        print(f'Pull request #{pr_number} merged successfully')
    else:
        print(f'Failed to merge pull request: {response.json()}')
    return response.json()

# Function to simulate contributions from developers
def simulate_developer_contributions():
    devs = [f'dev{i}' for i in range(1, 6)]

    # Create multiple commits for each developer on separate branches
    for dev in devs:
        branch_name = f'branch-{dev}'
        create_commit(f'{dev}/file1.txt', f'Initial commit by {dev}', f'Hello from {dev}!', branch=branch_name)
        create_commit(f'{dev}/file2.txt', f'Add more content by {dev}', f'More content from {dev}!', branch=branch_name)
        pr = create_pull_request(head_branch=branch_name)
        if pr:
            issue = create_issue(f'Issue for {dev}', f'This is an issue for {dev}', [dev])
            if issue:
                comment_issue(issue['number'], f'This is a comment by {dev}')
                close_issue(issue['number'])
                merge_pull_request(pr['number'])

if __name__ == '__main__':
    create_repository()
    simulate_developer_contributions()
