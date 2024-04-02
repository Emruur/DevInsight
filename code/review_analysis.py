import requests
import config
from dataclasses import dataclass
import csv

github_key = config.GITHUB_KEY

@dataclass
class Developer:
    """Class for keeping track of developer contributions."""
    name: str
    prs: dict = None

    def add_pull_request(self, pr_number, reviews, comments):
        if self.prs is None:
            self.prs = {}
        self.prs[pr_number] = {'reviews': reviews, 'comments': comments}

class GitDevelopers:
    def __init__(self, prs):
        self.devs = {}
        self.populate_git_developers(prs)

    def add_new_developer(self, name):
        self.devs[name] = Developer(name=name)

    def populate_git_developers(self, prs):
        for pr in prs:
            reviews = prs[pr]['reviews']
            comments = prs[pr]['comments']
            for review in reviews:
                author = review['author']
                if author not in self.devs:
                    self.add_new_developer(author)
                self.devs[author].add_pull_request(pr, reviews, comments)

    def display_pr_reviews(self, filtered_devs=None):
        for developer, dev_obj in self.devs.items():
            if filtered_devs and developer not in filtered_devs:
                continue
            print(f"Reviews and Comments by Developer: {developer}")
            print("-" * 60)
            for pr_number, data in dev_obj.prs.items():
                print(f"Pull Request #{pr_number}:")
                print("Reviews:")
                for review in data['reviews']:
                    print(f"\tAuthor: {review['author']}, State: {review['state']}, Text: {review['text']}")
                print("Comments:")
                for comment in data['comments']:
                    print(f"\tAuthor: {comment['author']}, Text: {comment['text']}")
                print("-" * 60)

    def create_reviews_csv(self, filtered_devs=None):
        for developer, dev_obj in self.devs.items():
            if filtered_devs and developer not in filtered_devs:
                continue
            with open(f"{developer}_reviews_and_comments.csv", mode='w') as csv_file:
                fieldnames = ['PR Number', 'Review Author', 'Review State', 'Review Text', 'Comment Author', 'Comment Text']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for pr_number, data in dev_obj.prs.items():
                    for review in data['reviews']:
                        for comment in data['comments']:
                            writer.writerow({'PR Number': pr_number, 
                                             'Review Author': review['author'], 
                                             'Review State': review['state'], 
                                             'Review Text': review['text'],
                                             'Comment Author': comment['author'], 
                                             'Comment Text': comment['text']})

def pr_reviews(token, owner, repo_name, max_prs=None):
    url = "https://api.github.com/graphql"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

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
        "owner": owner,
        "repoName": repo_name,
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
                    pr_reviews_dict[pr_number] = {'reviews': [], 'comments': []}
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

                # Check if there are more pages
                page_info = data['data']['repository']['pullRequests']['pageInfo']
                has_next_page = page_info['hasNextPage']

                if has_next_page:
                    variables['cursor'] = page_info['endCursor']
                else:
                    break

    return pr_reviews_dict

repo_url = "https://github.com/bumptech/glide"

# Extract repo owner and name from the URL
owner, repo_name = repo_url.split('/')[-2:]

reviews = pr_reviews(github_key, owner, repo_name)

git_devs = GitDevelopers(reviews)
git_devs.display_pr_reviews(filtered_devs=['michaeimm'])
git_devs.create_reviews_csv(filtered_devs=['michaeimm'])
