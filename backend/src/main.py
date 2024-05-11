import config
from GithubFetcher import GitHubFetcher
from Analysis import Analysis

key= config.GITHUB_KEY
repo_url = "https://github.com/Orange-OpenSource/hurl"
fetcher= GitHubFetcher(key, repo_url)

data = fetcher.fetch_data()

commits= data['developers_and_commits']
issues= data['all_issues']
prs= data['pr_reviews']
repo_name= data['repo_name']
date= data['timestamp']

analysis= Analysis(commits, issues, prs, date, repo_name)

analysis.save_analysis()





