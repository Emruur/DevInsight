import requests
import config
github_key = config.GITHUB_KEY

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
                    reviews = node['reviews']['edges']
                    pr_reviews_dict[pr_number] = []
                    for review in reviews:
                        review_node = review['node']
                        author = review_node['author']['login'] if review_node['author'] else 'Unknown'
                        state = review_node['state']
                        text = review_node['bodyText']
                        pr_reviews_dict[pr_number].append({'author': author, 'state': state, 'text': text})

                # Check if there are more pages
                page_info = data['data']['repository']['pullRequests']['pageInfo']
                has_next_page = page_info['hasNextPage']

                if has_next_page:
                    variables['cursor'] = page_info['endCursor']
                else:
                    break

    return pr_reviews_dict

def display_reviews(pr_reviews_dict):
    print("Pull Request Reviews:")
    print("-" * 60)
    for pr_number, reviews in pr_reviews_dict.items():
        print(f"Pull Request #{pr_number}:")
        for review in reviews:
            print(f"Author: {review['author']}, State: {review['state']}, Text: {review['text']}")
        print("-" * 60)

repo_url = "https://github.com/bumptech/glide"

# Extract repo owner and name from the URL
owner, repo_name = repo_url.split('/')[-2:]

reviews = pr_reviews(github_key, owner, repo_name)

# Display the reviews associated with pull requests
display_reviews(reviews)
