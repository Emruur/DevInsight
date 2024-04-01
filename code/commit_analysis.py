import requests
import config
from dataclasses import dataclass
from urllib.parse import urlparse

@dataclass
class Developer:
    """Class for keeping track of an item in inventory."""
    name: str
    username: str
    num_of_commits: int = 0
    num_of_add: int = 0
    num_of_delete: int = 0

@dataclass
class GitDevelopers:
    devs: dict[str, Developer]

def fetch_developers_and_commits(repo_url: str, token: str) -> GitDevelopers:
    """
    Fetches the developers and their commit counts in a repository using GraphQL.

    Args:
        repo_url (str): The URL of the repository.
        token (str): GitHub API token for authentication.

    Returns:
        GitDevelopers: Object containing developers and their commit counts.
    """
    parsed_url = urlparse(repo_url)
    path_parts = parsed_url.path.strip('/').split('/')
    if len(path_parts) != 2:
        print("Invalid repository URL")
        return GitDevelopers(devs={})

    owner, repo_name = path_parts
    query = """
    query {
      repository(owner: "%s", name: "%s") {
        defaultBranchRef {
          target {
            ... on Commit {
              history {
                edges {
                  node {
                    author {
                      name
                      user {
                        login
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    """ % (owner, repo_name)

    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }

    response = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if response.status_code == 200:
        data = response.json()
        devs = {}
        for edge in data['data']['repository']['defaultBranchRef']['target']['history']['edges']:
            author_name = edge['node']['author']['name']
            author_username = edge['node']['author']['user']['login'] if edge['node']['author']['user'] else None
            if author_name not in devs:
                devs[author_name] = Developer(name=author_name, username=author_username, num_of_commits=1)
            else:
                devs[author_name].num_of_commits += 1
        return GitDevelopers(devs=devs)
    else:
        print(f"Failed to fetch developers and commits for {repo_url}. Status code: {response.status_code}")
        return GitDevelopers(devs={})

# Example usage:
repo_url = "https://github.com/python-mode/python-mode"
github_token = config.TOKEN
git_developers = fetch_developers_and_commits(repo_url, github_token)
print("Developer Name\t\tGitHub Username\t\tNumber of Commits")
print("--------------------------------------------------------------")
for developer, data in git_developers.devs.items():
    print(f"{data.name}\t\t\t{data.username}\t\t\t{data.num_of_commits}")
