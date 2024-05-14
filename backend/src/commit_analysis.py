import requests
from dataclasses import dataclass
from urllib.parse import urlparse
from . import config
github_token= config.GITHUB_KEY

@dataclass
class DevCommits:
    """Class for keeping track of a developer's contributions."""
    name: str
    username: str
    num_of_commits: int = 0
    num_of_add: int = 0
    num_of_delete: int = 0
    num_of_files_changed: int = 0

@dataclass
class CommitAnalysis:
    devs: dict[str, DevCommits] = None

    def __init__(self, data):
        self.devs = {}
        self.initialize_devs(data)

    def initialize_devs(self, data):
        """Initializes developers from fetched data."""
        for edge in data:
            author_name = edge['node']['author']['name']
            author_username = edge['node']['author']['user']['login'] if edge['node']['author']['user'] else None
            additions = edge['node']['additions']
            deletions = edge['node']['deletions']
            files_changed = edge['node']['changedFiles']

            if author_name not in self.devs:
                self.devs[author_name] = DevCommits(name=author_name, username=author_username, num_of_commits=1,
                                                  num_of_add=additions, num_of_delete=deletions,
                                                  num_of_files_changed=files_changed)
            else:
                self.devs[author_name].num_of_commits += 1
                self.devs[author_name].num_of_add += additions
                self.devs[author_name].num_of_delete += deletions
                self.devs[author_name].num_of_files_changed += files_changed

    def get_contributors_as_json(self):
        contributors_json = {}
        for name, dev in self.devs.items():
            contributors_json[name] = {
                'Developer Name': dev.name,
                'GitHub Username': dev.username,
                'Number of Commits': dev.num_of_commits,
                'Additions': dev.num_of_add,
                'Deletions': dev.num_of_delete,
                'Files Changed': dev.num_of_files_changed
            }
        return contributors_json

    def __str__(self):
        contributors_json = self.get_contributors_as_json()
        
        # Determine the maximum lengths for dynamic column widths
        max_name_len = max(len(info['Developer Name']) for info in contributors_json.values())
        max_username_len = max(len(info['GitHub Username']) if info['GitHub Username'] else 0 for info in contributors_json.values())
        
        # Prepare the header with appropriate spacing
        header_format = "{:<" + str(max_name_len + 2) + "}{:<" + str(max_username_len + 2) + "}{:>15}{:>12}{:>12}{:>15}\n"
        header = header_format.format("Developer Name", "GitHub Username", "Number of Commits", "Additions", "Deletions", "Files Changed")
        header += "-" * (max_name_len + max_username_len + 56) + "\n"
        
        # Format each developer row
        row_format = "{:<" + str(max_name_len + 2) + "}{:<" + str(max_username_len + 2) + "}{:>15}{:>12}{:>12}{:>15}\n"
        for dev_info in contributors_json.values():
            header += row_format.format(dev_info['Developer Name'], dev_info['GitHub Username'] or '', 
                                        dev_info['Number of Commits'], dev_info['Additions'], 
                                        dev_info['Deletions'], dev_info['Files Changed'])

        return header

if __name__ == "__main__":
    # Example usage:
    repo_url = "https://github.com/python-mode/python-mode"
    #raw_data = fetch_developers_and_commits(repo_url, github_token)
    fetcher= GitHubFetcher(github_token,repo_url)
    raw_data= fetcher.fetch_developers_and_commits()

    # Initialize GitDevelopers with raw data
    git_developers = CommitAnalysis(raw_data)

    # Print summary
    print(git_developers)