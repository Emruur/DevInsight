from issue_analysis import IssueAnalysis
from commit_analysis import CommitAnalysis
from review_analysis import SentimentalAnalysis
import json
import datetime

class Analysis:
    def __init__(self, commits, issues, prs, date, repo_name) -> None:
        self.date = date
        self.repo_name = repo_name
        self.issue_analysis = IssueAnalysis(issues)
        self.commit_analysis = CommitAnalysis(commits)
        self.pr_analysis = SentimentalAnalysis(prs)

    def save_analysis(self) -> None:
        # Format the filename as 'repo_name_date.json', including only up to the hour
        filename = f"analysis/{self.repo_name}_{self.date}.json"

        # Collecting data from each analysis component
        data = {
            "date": self.date,
            "repo_name": self.repo_name,
            "issues": self.issue_analysis.get_dev_stats_as_json(),
            "commits": self.commit_analysis.get_contributors_as_json(),
            "prs": self.pr_analysis.get_developers_as_json()
        }

        # Writing data to a JSON file
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

        print(f"Analysis saved to {filename}")
