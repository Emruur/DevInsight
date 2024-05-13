import requests
from urllib.parse import urlparse
import json
from . import config
import os 
from datetime import datetime
from src.issue_analysis import IssueAnalysis
from src.commit_analysis import CommitAnalysis
from src.review_analysis import SentimentalAnalysis


class GitHubFetcher:
    def __init__(self, token, repo_url):
        self.token = token
        
        self.owner, self.repo_name = self._parse_repo_url(repo_url)
        self.base_url = 'https://api.github.com/graphql'
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    def save_data(self):
        """
        Fetches all data using existing functions, adds a timestamp, and saves it into a JSON file.
        The file is named after the repository, includes a timestamp, and is stored under a directory named 'fetched_data'.
        """
        # Fetch the data
        developers_and_commits = self.get_dev_commits()
        all_issues = self.get_repo_issues()
        pr_reviews = self.get_repo_prs()

        # Add a timestamp to the data
        timestamp = datetime.now().isoformat()
        data = {
            'timestamp': timestamp,
            'developers_and_commits': developers_and_commits,
            'all_issues': all_issues,
            'pr_reviews': pr_reviews
        }

        # Create the 'fetched_data' directory if it doesn't exist
        directory = "fetched_data"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Define the file path within the 'fetched_data' directory
        file_name = f"{self.repo_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
        file_path = os.path.join(directory, file_name)

        # Write the data to a JSON file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Data saved to {file_path}")

    def fetch_saved_data(self):
        """
        Fetches saved data from a JSON file within the 'fetched_data' directory.
        
        
        Returns:
            dict: The data retrieved from the file, or None if the file does not exist.
        """
        # List all files in the 'fetched_data' directory
        directory = "fetched_data"
        files = os.listdir(directory)

        # Find the most recent file for the specified repository
        latest_file = None
        latest_time = None
        for file in files:
            if file.startswith(self.repo_name) and file.endswith('.json'):
                file_time_str = file[len(self.repo_name)+1:-5]  # Extract timestamp from filename
                file_time = datetime.strptime(file_time_str, '%Y-%m-%d_%H-%M-%S')
                if latest_time is None or file_time > latest_time:
                    latest_time = file_time
                    latest_file = file

        # If a file is found, read and return its content
        if latest_file:
            file_path = os.path.join(directory, latest_file)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        else:
            print(f"No saved data found for the repository '{self.repo_name}'.")
            return None
        
    def fetch_data(self, app, repo_name):
        """
        Fetches all data related to developers, issues, and pull requests for the specified repository,
        adds a timestamp and repository name, and returns it.
        """
        # Fetch the data
        app.logger.debug(f"Data fetcimg for {repo_name}")
        developers_and_commits = self.get_dev_commits()
        app.logger.debug(f"Commits fetched for {repo_name}")
        all_issues = self.get_repo_issues()
        app.logger.debug(f"Issues fetched for {repo_name}")
        pr_reviews = self.get_repo_prs(app,repo_name)
        app.logger.debug(f"PR's fetched for {repo_name}")


        # Add a timestamp and repository name to the data
        timestamp = datetime.now().date().isoformat()
        data = {
            'timestamp': timestamp,
            'repo_name': self.repo_name,
            'developers_and_commits': developers_and_commits,
            'all_issues': all_issues,
            'pr_reviews': pr_reviews
        }

        return data
        
    def _parse_repo_url(self, repo_url):
        parsed_url = urlparse(repo_url)
        path_parts = parsed_url.path.strip('/').split('/')
        if len(path_parts) != 2:
            raise ValueError("Invalid repository URL")
        return path_parts

    def get_dev_commits(self):

        query = f"""
        query {{
          repository(owner: "{self.owner}", name: "{self.repo_name}") {{
            defaultBranchRef {{
              target {{
                ... on Commit {{
                  history {{
                    edges {{
                      node {{
                        author {{
                          name
                          user {{
                            login
                          }}
                        }}
                        additions
                        deletions
                        changedFiles
                      }}
                    }}
                  }}
                }}
              }}
            }}
          }}
        }}
        """

        response = requests.post(self.base_url, json={'query': query}, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch developers and commits. Status code: {response.status_code} - {response.message}")

    def get_repo_issues(self, max_issues=None):
        all_issues = []
        issues_cursor = None
        query_template = """
        query ($owner: String!, $repoName: String!, $count: Int!, $issuesCursor: String) {
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
        }
        }
        """

        while True:
            issues_fetch_count = 100 if max_issues is None else min(100, max_issues - len(all_issues))
            variables = {'owner': self.owner, 'repoName': self.repo_name, 'count': issues_fetch_count, 'issuesCursor': issues_cursor}

            response = requests.post(self.base_url, json={'query': query_template, 'variables': variables}, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                issues = data['data']['repository']['issues']['edges']
                all_issues.extend(issues[:issues_fetch_count])
                if len(issues) == issues_fetch_count and data['data']['repository']['issues']['pageInfo']['hasNextPage']:
                    issues_cursor = issues[-1]['cursor']
                else:
                    issues_cursor = None

                if issues_cursor is None or (max_issues is not None and len(all_issues) >= max_issues):
                    break
            else:
                raise Exception(f"Issue query failed to run with a {response.status_code} - {response.message}")

        return all_issues[:max_issues]

    def get_repo_prs(self, app, repo_name):
        url = "https://api.github.com/graphql"
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

        # GraphQL query template to fetch pull requests and associated reviews
        query_template = """
        query ($owner: String!, $repoName: String!, $numPullRequests: Int!, $cursor: String) {
            repository(owner: $owner, name: $repoName) {
                pullRequests(first: $numPullRequests, after: $cursor) {
                    edges {
                        node {
                            title
                            url
                            createdAt
                            number
                            commits(first: 100) {
                                edges {
                                    node {
                                        commit {
                                            author {
                                                user {
                                                    login
                                                }
                                            }   
                                        }
                                    }
                                }
                            }
                            comments(first: 100) {
                                edges {
                                    node {
                                        author {
                                            login
                                        }
                                        bodyText
                                    }
                                }
                            }
                            reviews(first: 100) {
                                edges {
                                    node {
                                        author {
                                            login
                                        }
                                        state
                                        bodyText
                                    }
                                }
                            }
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
        pr_reviews_dict = {}
        variables = {
            "owner": self.owner,
            "repoName": self.repo_name,
            "numPullRequests": 100,  # Initial batch size, capped at 100
            "cursor": None
        }
        app.logger.debug(f"Fetching prs for {repo_name}")
        cnt= 1
        while True:
            app.logger.debug(f" PR Fetching page {cnt} for {repo_name} with {variables}")
            response = requests.post(url, json={'query': query_template, 'variables': variables}, headers=headers)
            app.logger.debug(f" returned {cnt}")

            if response.status_code != 200:
                app.logger.debug(f"PR query failed to run with a {response.status_code}")
                app.logger.debug(f"PR query failed message {response.text}")
                break
            else:
                
                data = response.json()
                if 'errors' in data:
                    app.logger.debug("GraphQL query returned errors:")
                    for error in data['errors']:
                        print(error['message'])
                        app.logger.debug(f"PR error query {error['message']}")
                    break
                else:
                    app.logger.debug(f" PR fetch finished {cnt} for {repo_name}")
                    cnt += 1
                    pull_requests = data['data']['repository']['pullRequests']['edges']
                    for pr in pull_requests:
                        node = pr['node']
                        pr_number = node['number']
                        comments = node['comments']['edges']
                        reviews = node['reviews']['edges']
                        commits = node['commits']['edges']
                        pr_reviews_dict[pr_number] = {'reviews': [], 'comments': [], 'commits': []}  # Ensure 'commits' key is initialized
                        for review in reviews:
                            review_node = review['node']
                            author = review_node['author']['login'] if review_node['author'] else 'Unknown'
                            state = review_node['state']
                            text = review_node['bodyText']
                            pr_reviews_dict[pr_number]['reviews'].append({'author': author, 'state': state, 'text': text})

                        for comment in comments:
                            comment_node = comment['node']
                            author = comment_node['author']['login'] if comment_node['author'] else 'Unknown'
                            text = comment_node['bodyText']
                            pr_reviews_dict[pr_number]['comments'].append({'author': author, 'text': text})    

                        for commit in commits:
                            commit_node = commit['node']
                            author_login = None
                            if commit_node['commit']['author']['user'] is not None:
                                author_login = commit_node['commit']['author']['user']['login']
                            pr_reviews_dict[pr_number]['commits'].append(author_login)


                    # Check if there are more pages
                    page_info = data['data']['repository']['pullRequests']['pageInfo']
                    has_next_page = page_info['hasNextPage']

                    if has_next_page:
                        variables['cursor'] = page_info['endCursor']
                    else:
                        app.logger.debug(f" no more PR pages for {repo_name} ")
                        break

        return pr_reviews_dict






