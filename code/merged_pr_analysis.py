import requests
import config
github_key = config.GITHUB_KEY

def merged_prs(token, owner, repo_name, max_prs=None):
    url = "https://api.github.com/graphql"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # GraphQL query template to fetch merged PRs
    query_template = """
    query ($owner: String!, $repoName: String!, $numPullRequests: Int!, $cursor: String) {
        repository(owner: $owner, name: $repoName) {
            pullRequests(states: MERGED, first: $numPullRequests, after: $cursor) {
                edges {
                    node {
                        title
                        url
                        createdAt
                        number
                        mergedBy {
                            login
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

    all_prs = []
    variables = {
        "owner": owner,
        "repoName": repo_name,
        "numPullRequests": 100,  # page size
        "cursor": None
    }

    merged_pull_requests = []
    while True:
        response = requests.post(url, json={'query': query_template, 'variables': variables}, headers=headers)

        if response.status_code != 200:
            print(f"Query failed to run with a {response.status_code}")
            break
        else:
            data = response.json()
            if 'errors' in data:
                for error in data['errors']:
                    print(error['message'])
                break
            else:
                pull_requests = data['data']['repository']['pullRequests']['edges']
                for pr in pull_requests:
                    node = pr['node']
                    merged_pull_requests.append(node)

                # next page
                page_info = data['data']['repository']['pullRequests']['pageInfo']
                has_next_page = page_info['hasNextPage']

                if has_next_page:
                    variables['cursor'] = page_info['endCursor']
                else:
                    break

    return merged_pull_requests[:max_prs]

def display_prs(prs):
    print("Fetched Pull Requests:")
    print("-" * 60)
    i = 1
    for pr in prs:
        print(f"PR {i}")
        i += 1
        title = pr.get('title', 'No Title')
        url = pr.get('url', 'No URL')
        created_at = pr.get('createdAt', 'No Creation Date')
        number = pr.get('number', 'No Number')
        merged_by = pr['mergedBy']['login'] if pr.get('mergedBy') else 'Unknown'
        # Print the details of each PR
        print(f"Title: {title}")
        print(f"URL: {url}")
        print(f"Created At: {created_at}")
        print(f"PR Number: {number}")
        print(f"Merged By: {merged_by}")
        print("-" * 60)

def count_merged_by_developer(prs):
    developer_counts = {}
    for pr in prs:
        merged_by = pr['mergedBy']['login'] if pr.get('mergedBy') else 'Unknown'
        developer_counts[merged_by] = developer_counts.get(merged_by, 0) + 1
    return developer_counts

def display_merged_counts(counts):
    print("Merged PRs by Developer:")
    print("-" * 60)
    for developer, count in counts.items():
        print(f"{developer}: {count}")
    print("-" * 60)

repo_url = "https://github.com/bumptech/glide"

# Extract repo owner and name from the URL
owner, repo_name = repo_url.split('/')[-2:]

prs = merged_prs(github_key, owner, repo_name, max_prs=None)

# Display the fetched PRs
display_prs(prs)


# Count merged PRs by developer
merged_counts = count_merged_by_developer(prs)

# Display the count of merged PRs by each developer
display_merged_counts(merged_counts)