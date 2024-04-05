import requests
from urllib.parse import urlparse

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
        
    def _parse_repo_url(self, repo_url):
        parsed_url = urlparse(repo_url)
        path_parts = parsed_url.path.strip('/').split('/')
        if len(path_parts) != 2:
            raise ValueError("Invalid repository URL")
        return path_parts

    def fetch_developers_and_commits(self):

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
            raise Exception(f"Failed to fetch developers and commits. Status code: {response.status_code}")

    def fetch_all_issues(self, max_issues=None):
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
                raise Exception(f"Query failed to run with a {response.status_code}")

        return all_issues[:max_issues]

    def pr_reviews(self):
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

        while True:
            response = requests.post(url, json={'query': query_template, 'variables': variables}, headers=headers)

            if response.status_code != 200:
                print(f"Query failed to run with a {response.status_code}")
                break
            else:
                data = response.json()
                if 'errors' in data:
                    print("GraphQL query returned errors:")
                    for error in data['errors']:
                        print(error['message'])
                    break
                else:
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
                        break

        return pr_reviews_dict

    def _build_pr_query(self):
        # GraphQL query template to fetch pull requests and associated reviews
        return """
        query ($owner: String!, $repoName: String!, $numPullRequests: Int!, $cursor: String) {{
            repository(owner: $owner, name: $repoName) {{
                pullRequests(first: $numPullRequests, after: $cursor) {{
                    edges {{
                        node {{
                            title
                            url
                            createdAt
                            number
                            commits(first: 100) {{
                                edges {{
                                    node {{
                                        commit {{
                                            author {{
                                                user {{
                                                    login
                                                }}
                                            }}   
                                        }}
                                    }}
                                }}
                            }}
                            comments(first: 100) {{
                                edges {{
                                    node {{
                                        author {{
                                            login
                                        }}
                                        bodyText
                                    }}
                                }}
                            }}
                            reviews(first: 100) {{
                                edges {{
                                    node {{
                                        author {{
                                            login
                                        }}
                                        state
                                        bodyText
                                    }}
                                }}
                            }}
                        }}
                        cursor
                    }}
                    pageInfo {{
                        endCursor
                        hasNextPage
                    }}
                }}
            }}
        }}
        """

    def _process_pull_request(self, pr, pr_reviews_dict):
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
