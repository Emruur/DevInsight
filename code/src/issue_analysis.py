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
class DevIssues:
    """Class for keeping track of developer contributions."""
    name: str
    num_of_issues_created: int = 0
    num_of_issues_assigned: int = 0
    num_of_issues_resolved: int = 0  # Track the number of issues resolved by the developer
    total_resolution_time: float = 0.0  # Total time to resolve issues in hours

    @property
    def average_issue_resolution_time(self):
        if self.num_of_issues_resolved > 0:  # Calculate average based on resolved issues
            return self.total_resolution_time / self.num_of_issues_resolved
        else:
            return 0
        
    def update_resolution_metrics(self, resolution_time):
        if resolution_time is not None:
            self.num_of_issues_resolved += 1
            self.total_resolution_time += resolution_time


class IssueAnalysis:
    def __init__(self, issues):
        self.devs = {}
        self.populate_git_developers(issues)

    def add_new_developer(self, name):
        self.devs[name] = DevIssues(name=name)

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
                    #print(f"Start: {created_at} End: {closed_at}")
            elif resolution_time is not None:
                #TODO what do we do in case of no assignees, should we add this to the creator?
                pass

    def get_dev_stats_as_json(self, filter_assignees=False):
        dev_stats = {}
        for name, dev in self.devs.items():
            if filter_assignees and dev.num_of_issues_assigned == 0:
                continue
            dev_stats[name] = {
                'Number of Issues Created': dev.num_of_issues_created,
                'Number of Issues Assigned': dev.num_of_issues_assigned,
                'Number of Issues Resolved': dev.num_of_issues_resolved,
                'Average Issue Resolution Time': round(dev.average_issue_resolution_time, 2)
            }
        return dev_stats

    def __str__(self, filter_assignees=False):
        dev_stats = self.get_dev_stats_as_json(filter_assignees)
        display_str = "GitHub Developers' Statistics:\n"
        display_str += "-" * 80 + "\n"
        for name, stats in dev_stats.items():
            display_str += f"Developer Name: {name}\n"
            display_str += '\n'.join([f"{k}: {v}" for k, v in stats.items()])
            display_str += "\n" + "-" * 80 + "\n"
        return display_str


if __name__ == "main":
    repo_url = "https://github.com/dbeaver/dbeaver"

    fetcher= GitHubFetcher(github_key, repo_url)
    all_issues= fetcher.fetch_all_issues()

    dev_info= IssueAnalysis(all_issues)

    dev_info.display(filter_assignees=True)




