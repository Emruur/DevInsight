import requests
from dataclasses import dataclass
from urllib.parse import urlparse
import config
from GithubFetcher import GitHubFetcher
github_token= config.GITHUB_KEY

@dataclass
class Developer:
    """Class for keeping track of a developer's contributions."""
    name: str
    username: str
    num_of_commits: int = 0
    num_of_add: int = 0
    num_of_delete: int = 0
    num_of_files_changed: int = 0

@dataclass
class GitDevelopers:
    devs: dict[str, Developer] = None

    def __init__(self, data):
        self.devs = {}
        self.initialize_devs(data)

    def initialize_devs(self, data):
        """Initializes developers from fetched data."""
        for edge in data['data']['repository']['defaultBranchRef']['target']['history']['edges']:
            author_name = edge['node']['author']['name']
            author_username = edge['node']['author']['user']['login'] if edge['node']['author']['user'] else None
            additions = edge['node']['additions']
            deletions = edge['node']['deletions']
            files_changed = edge['node']['changedFiles']

            if author_name not in self.devs:
                self.devs[author_name] = Developer(name=author_name, username=author_username, num_of_commits=1,
                                                  num_of_add=additions, num_of_delete=deletions,
                                                  num_of_files_changed=files_changed)
            else:
                self.devs[author_name].num_of_commits += 1
                self.devs[author_name].num_of_add += additions
                self.devs[author_name].num_of_delete += deletions
                self.devs[author_name].num_of_files_changed += files_changed

    def __str__(self):
        # Determine the maximum lengths for dynamic column widths
        max_name_len = max(len(dev.name) for dev in self.devs.values())
        max_username_len = max(len(dev.username) if dev.username else 0 for dev in self.devs.values())

        # Prepare the header with appropriate spacing
        header_format = "{:<" + str(max_name_len + 2) + "}{:<" + str(max_username_len + 2) + "}{:>15}{:>12}{:>12}{:>15}\n"
        header = header_format.format("Developer Name", "GitHub Username", "Number of Commits", "Additions", "Deletions", "Files Changed")
        header += "-" * (max_name_len + max_username_len + 56) + "\n"

        # Format each developer row
        row_format = "{:<" + str(max_name_len + 2) + "}{:<" + str(max_username_len + 2) + "}{:>15}{:>12}{:>12}{:>15}\n"
        for developer, data in self.devs.items():
            header += row_format.format(data.name, data.username or '', data.num_of_commits, data.num_of_add, data.num_of_delete, data.num_of_files_changed)

        return header

# Example usage:
repo_url = "https://github.com/python-mode/python-mode"
#raw_data = fetch_developers_and_commits(repo_url, github_token)
fetcher= GitHubFetcher(github_token,repo_url)
raw_data= fetcher.fetch_developers_and_commits()

# Initialize GitDevelopers with raw data
git_developers = GitDevelopers(raw_data)

# Print summary
print(git_developers)