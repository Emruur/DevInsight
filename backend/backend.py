from flask import Flask, jsonify, request, abort
import os
import json
from src.GithubFetcher import GitHubFetcher
from src.Analysis import Analysis
from src import config
from datetime import datetime
from flask_executor import Executor
import logging
from flask_cors import CORS
from urllib.parse import urlparse
import requests
from urllib.parse import urlparse, urlsplit

app = Flask(__name__)
CORS(app)
executor = Executor(app)

analysis_directory = "analysis"  # Update with the path to the analysis directory
in_progress_directory = "in_progress"  # Update with the path to the in_progress directory


def check_repository_exists(repo_url):
    """
    Check if a GitHub repository exists by parsing its URL.

    Args:
    repo_url (str): The full URL to the GitHub repository.

    Returns:
    bool: True if the repository exists, False otherwise.
    """
    if repo_url[-1]== "/":
        return False
    parts = urlsplit(repo_url)
    path = parts.path.strip('/').split('/')
    if len(path) != 2 or parts.netloc not in ['github.com', 'www.github.com']:
        return False

    owner, repo_name = path
    url = f"https://api.github.com/repos/{owner}/{repo_name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        return False

# Helper function to validate URLs using urllib.parse
def is_valid_url(url):
    try:
        parsed = urlparse(url)
        return all([parsed.scheme, parsed.netloc])
    except ValueError:
        return False

@app.route("/get_all_analysis", methods=['GET'])
def get_all_analysis():
    analyses = {}
    # Gather completed analyses
    for filename in os.listdir(analysis_directory):
        if filename.endswith(".json"):  # Ensure only JSON files are processed
            repo_name, date = filename.split('_')[0], filename.split('_')[1].split('.')[0]
            if repo_name in analyses:
                analyses[repo_name].append(date)
            else:
                analyses[repo_name] = [date]

    # Mark in-progress analyses
    for filename in os.listdir(in_progress_directory):
        if filename.endswith(".json"):  # Consistency in file type handling
            repo_name = filename.split('.')[0]
            if repo_name in analyses:
                # Preserves any completed analysis dates already listed
                analyses[repo_name].append('in progress')
            else:
                analyses[repo_name] = ['in progress']

    # Convert dictionary to array of objects
    response = [{'repo_name': key, 'dates': value} for key, value in analyses.items()]
    return jsonify(response)

@app.route("/get_analysis/<string:repo_name>/<string:date>", methods=['GET'])
def get_analysis(repo_name, date):
    file_path = f"{analysis_directory}/{repo_name}_{date}.json"
    if not os.path.exists(file_path):
        if os.path.exists(f"{in_progress_directory}/{repo_name}.json"):
            return jsonify({"error": "Analysis is in progress for this repository"}), 404
        return jsonify({"error": "Analysis not found"}), 404
    with open(file_path, 'r') as file:
        data = json.load(file)
    return jsonify(data)

def file_exists(directory, filename):
    return os.path.exists(os.path.join(directory, filename))

def perform_analysis(repo_name, repo_url):
    app.logger.debug(f"Analysis started for {repo_name}")
    key = config.GITHUB_KEY
    fetcher = GitHubFetcher(key, repo_url)
    data = fetcher.fetch_data(app, repo_name)
    app.logger.debug(f"Data fetched for {repo_name}")
    
    analysis = Analysis(data['developers_and_commits'], data['all_issues'], data['pr_reviews'], data['timestamp'], repo_name)
    analysis.save_analysis()

    # Remove the in-progress file after completion
    os.remove(os.path.join(in_progress_directory, f"{repo_name}.json"))
    app.logger.debug(f"Analysis finished for {repo_name}")
    return {"message": "Analysis completed successfully for " + repo_name}

@app.route("/create_analysis", methods=['POST'])
def create_analysis():
    repo_url = request.json.get('repo_url')
    if not repo_url:
        return jsonify({"error": "Repository URL is required."}), 400
    if not is_valid_url(repo_url):
        return jsonify({"error": "Invalid Repository URL."}), 400
    
    if not check_repository_exists(repo_url):
        return jsonify({"error": "Repository does not exists."}), 400
    
    repo_name = repo_url.split('/')[-1]
    in_progress_path = os.path.join(in_progress_directory, f"{repo_name}.json")
    if any(os.listdir(in_progress_directory)):
        return jsonify({"error": f"An analysis is already in progress"}), 400
    
    today_str = datetime.now().strftime('%Y-%m-%d')
    if file_exists(analysis_directory, f"{repo_name}_{today_str}.json"):
        return jsonify({"error": f"An analysis already exists for {today_str}"}), 400

    with open(in_progress_path, 'w') as file:
        json.dump({"status": "in progress", "repo_url": repo_url}, file)

    executor.submit(perform_analysis, repo_name, repo_url)
        
    #perform_analysis(repo_name, repo_url)
    return jsonify({"message": "Analysis started successfully for " + repo_name}), 202


if __name__ == '__main__':
    app.run(debug=True)