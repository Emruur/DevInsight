import requests
import google.generativeai as genai
import config
import requests
from dataclasses import dataclass
from datetime import datetime

# Use the API keys from config.py
github_key = config.GITHUB_KEY
gemini_key = config.GEMINI_KEY

@dataclass
class Developer:
    """Class for keeping track of developer contributions."""
    name: str
    num_of_issues_created: int = 0
    num_of_issues_assigned: int = 0
    num_of_issues_resolved: int = 0  # Track the number of issues resolved by the developer
    total_resolution_time: float = 0.0  # Total time to resolve issues in hours
    average_issue_resolution_time: float = 0.0  # Average time to resolve an issue in hours

    def update_resolution_metrics(self, resolution_time):
        if resolution_time is not None:
            self.num_of_issues_resolved += 1
            self.total_resolution_time += resolution_time
            if self.num_of_issues_resolved > 0:  # Calculate average based on resolved issues
                self.average_issue_resolution_time = self.total_resolution_time / self.num_of_issues_resolved

class GitDevelopers:
    def __init__(self, issues):
        self.devs = {}
        self.populate_git_developers(issues)

    def add_new_developer(self, name):
        self.devs[name] = Developer(name=name)

    def update_developer(self, name, issue_created=False, issue_assigned=False, resolution_time=None):
        if issue_created:
            self.devs[name].num_of_issues_created += 1

        if issue_assigned:
            self.devs[name].num_of_issues_assigned += 1

        if resolution_time is not None:
            self.devs[name].update_resolution_metrics(resolution_time)





    def populate_git_developers(self, issues):
        for issue in issues:
            node = issue['node']
            creator = node['author']['login'] if node['author'] else 'Unknown'
            created_at = datetime.strptime(node['createdAt'], '%Y-%m-%dT%H:%M:%SZ')
            closed_at = datetime.strptime(node['closedAt'], '%Y-%m-%dT%H:%M:%SZ') if node['closedAt'] else None

            resolution_time = (closed_at - created_at).total_seconds() / 3600.0 if closed_at else None

            if creator not in self.devs:
                self.add_new_developer(creator)
            self.update_developer(name=creator, issue_created=True)

            assignees = [assignee['node']['login'] for assignee in node['assignees']['edges']]
            if 'assignees' in node and node['assignees']['edges']:  # Check if assignees exist
                assignees = [assignee['node']['login'] for assignee in node['assignees']['edges']]
                for assignee in assignees:
                    if assignee not in self.devs:
                        self.add_new_developer(assignee)
                    # Assignee is considered as the resolver, so update with resolution time
                    self.update_developer(name=assignee, issue_assigned=True, resolution_time=resolution_time)
            elif resolution_time is not None:
                #TODO what do we do in case of no assignees, should we add this to the creator?
                pass

    def display(self, filter_assignees= False):
        print("GitHub Developers' Statistics:")
        print("-" * 80)
        for name, dev in self.devs.items():
            if filter_assignees and dev.num_of_issues_assigned == 0:
                continue
            print(f"Developer Name: {name}")
            print(f"Number of Issues Created: {dev.num_of_issues_created}")
            print(f"Number of Issues Assigned: {dev.num_of_issues_assigned}")
            print(f"Number of Issues Resolved: {dev.num_of_issues_resolved}")
            print(f"Average Issue Resolution Time (hours): {dev.average_issue_resolution_time:.2f}")
            print("-" * 80)

# Example usage:
# issues = [...]  # Your list of issues here
# git_devs = GitDevelopers(issues)
# git_devs.display()


def fetch_all_issues_and_prs(token, owner, repo_name, max_issues=None, max_prs=None):
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
            closedAt
            state
            author {
                login
            }
            assignees(first: 10) {
                edges {
                node {
                    login
                }
                }
            }
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
        # Calculate fetch count based on remaining items to reach max_issues or max_prs
        issues_fetch_count = 100 if max_issues is None else min(100, max_issues - len(all_issues))
        prs_fetch_count = 100 if max_prs is None else min(100, max_prs - len(all_prs))

        variables = {'owner': owner, 'repoName': repo_name, 'count': max(issues_fetch_count, prs_fetch_count), 'issuesCursor': issues_cursor, 'prsCursor': prs_cursor}

        response = requests.post(url, json={'query': query_template, 'variables': variables}, headers=headers)
        if response.status_code == 200:
            data = response.json()

            # Process issues
            issues = data['data']['repository']['issues']['edges']
            all_issues.extend(issues[:issues_fetch_count])
            if len(issues) == issues_fetch_count and data['data']['repository']['issues']['pageInfo']['hasNextPage']:
                issues_cursor = issues[-1]['cursor']
            else:
                issues_cursor = None

            # Process PRs
            prs = data['data']['repository']['pullRequests']['edges']
            all_prs.extend(prs[:prs_fetch_count])
            if len(prs) == prs_fetch_count and data['data']['repository']['pullRequests']['pageInfo']['hasNextPage']:
                prs_cursor = prs[-1]['cursor']
            else:
                prs_cursor = None

            if (issues_cursor is None or (max_issues is not None and len(all_issues) >= max_issues)) and \
               (prs_cursor is None or (max_prs is not None and len(all_prs) >= max_prs)):
                # No more pages for both issues and PRs, or max limit reached
                break
        else:
            print(f"Query failed to run with a {response.status_code}")
            break

    return all_issues[:max_issues], all_prs[:max_prs]
def display_issues_and_prs(issues, prs):
    print("GitHub Issues:")
    print("-" * 60)
    for issue in issues:
        node = issue['node']
        print(f"Title: {node['title']}")
        print(f"URL: {node['url']}")
        print(f"Created At: {node['createdAt']}")
        print(f"Closed At: {node['closedAt'] if node['closedAt'] else 'Not Closed'}")
        print(f"State: {node['state']}")
        print(f"Author: {node['author']['login'] if node['author'] else 'Unknown'}")

        assignees = [assignee['node']['login'] for assignee in node['assignees']['edges']]
        print(f"Assignees: {', '.join(assignees) if assignees else 'None'}")

        print(f"Issue Number: {node['number']}")
        print("-" * 60)

    print("\nGitHub Pull Requests:")
    print("-" * 60)
    for pr in prs:
        node = pr['node']
        print(f"Title: {node['title']}")
        print(f"URL: {node['url']}")
        print(f"Created At: {node['createdAt']}")
        print(f"PR Number: {node['number']}")
        print("-" * 60)


repo_url = "https://github.com/dbeaver/dbeaver"

# Extract repo owner and name from the URL
owner, repo_name = repo_url.split('/')[-2:]

# Fetch merged PRs
all_issues, all_prs = fetch_all_issues_and_prs(github_key, owner, repo_name, max_issues=2000, max_prs=0)

dev_info= GitDevelopers(all_issues)

dev_info.display(filter_assignees=True)




