import requests
import config
from dataclasses import dataclass
from urllib.parse import urlparse

@dataclass
class Developer:
    """Class for keeping track of an item in inventory."""
    name: str
    num_of_commits: int=0
    num_of_add: int=0
    num_of_delete:int= 0

@dataclass
class GitDevelopers:
    devs: dict[str, Developer]

def fetch_commits(repo_url: str, token: str) -> int:
    """
    Fetches the number of commits in a repository using GraphQL.

    Args:
        repo_url (str): The URL of the repository.
        token (str): GitHub API token for authentication.

    Returns:
        int: The number of commits in the repository.
    """
    parsed_url = urlparse(repo_url)
    path_parts = parsed_url.path.strip('/').split('/')
    if len(path_parts) != 2:
        print("Invalid repository URL")
        return 0

    owner, repo_name = path_parts
    query = """
    query {
      repository(owner: "%s", name: "%s") {
        defaultBranchRef {
          target {
            ... on Commit {
              history {
                totalCount
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
        num_commits = data['data']['repository']['defaultBranchRef']['target']['history']['totalCount']
        return num_commits
    else:
        print(f"Failed to fetch commits for {repo_url}. Status code: {response.status_code}")
        return 0

# Example usage:
repo_url = "https://github.com/NationalSecurityAgency/ghidra"
github_token = config.TOKEN
num_commits = fetch_commits(repo_url, github_token)
print(f"Number of commits in {repo_url}: {num_commits}")
