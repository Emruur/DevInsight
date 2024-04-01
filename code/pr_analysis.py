import requests
import config

github_key = config.GITHUB_KEY

def fetch_all_prs(token, owner, repo_name, max_prs=None):
    url = 'https://api.github.com/graphql'
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

    # GraphQL query template to fetch PRs
    query_template = """
    query ($owner: String!, $repoName: String!, $count: Int!, $prsCursor: String) {
    repository(owner: $owner, name: $repoName) {
        pullRequests(first: $count, after: $prsCursor) {
        edges {
            node {
            title
            url
            createdAt
            number
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
    prs_cursor = None

    while True:
        prs_fetch_count = 100 if max_prs is None else min(100, max_prs - len(all_prs))
        variables = {'owner': owner, 'repoName': repo_name, 'count': prs_fetch_count, 'prsCursor': prs_cursor}

        response = requests.post(url, json={'query': query_template, 'variables': variables}, headers=headers)
        if response.status_code == 200:
            data = response.json()
            prs = data['data']['repository']['pullRequests']['edges']
            all_prs.extend(prs[:prs_fetch_count])
            if len(prs) == prs_fetch_count and data['data']['repository']['pullRequests']['pageInfo']['hasNextPage']:
                prs_cursor = prs[-1]['cursor']
            else:
                prs_cursor = None

            if prs_cursor is None or (max_prs is not None and len(all_prs) >= max_prs):
                break
        else:
            print(f"Query failed to run with a {response.status_code}")
            break

    return all_prs[:max_prs]

def display_prs(prs):
    print("Fetched Pull Requests:")
    print("-" * 60)
    for pr in prs:
        node = pr['node']  # Extract the PR node
        title = node.get('title', 'No Title')
        url = node.get('url', 'No URL')
        created_at = node.get('createdAt', 'No Creation Date')
        number = node.get('number', 'No Number')
        # Print the details of each PR
        print(f"Title: {title}")
        print(f"URL: {url}")
        print(f"Created At: {created_at}")
        print(f"PR Number: {number}")
        print("-" * 60)


repo_url = "https://github.com/dbeaver/dbeaver"

# Extract repo owner and name from the URL
owner, repo_name = repo_url.split('/')[-2:]

# Fetch the PRs
prs = fetch_all_prs(github_key, owner, repo_name, max_prs=100)

# Display the fetched PRs
display_prs(prs)
