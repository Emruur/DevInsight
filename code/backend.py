from flask import Flask, jsonify, request, abort
import os
import json

app = Flask(__name__)

analysis_directory = "analysis"  # Update with the path to the analysis directory
in_progress_directory = "in_progress"  # Update with the path to the in_progress directory

@app.route("/get_all_analysis", methods=['GET'])
def get_all_analysis():
    analyses = {}
    for filename in os.listdir(analysis_directory):
        repo_name, date = filename.split('_')[0], filename.split('_')[1].split('.')[0]
        if repo_name in analyses:
            analyses[repo_name].append(date)
        else:
            analyses[repo_name] = [date]
    for filename in os.listdir(in_progress_directory):
        repo_name = filename.split('.')[0]
        analyses[repo_name] = "in_progress"
    return jsonify(analyses)

@app.route("/get_analysis/<string:repo_name>/<string:date>", methods=['GET'])
def get_analysis(repo_name, date):
    file_path = f"{analysis_directory}/{repo_name}_{date}.json"
    if not os.path.exists(file_path):
        if os.path.exists(f"{in_progress_directory}/{repo_name}.json"):
            return jsonify({"error": "Analysis is in progress for this repository"}), 404
        return jsonify({"error": "File not found"}), 404
    with open(file_path, 'r') as file:
        data = json.load(file)
    return jsonify(data)

@app.route("/create_analysis", methods=['POST'])
def create_analysis():
    repo_url = request.json['repo_url']
    repo_name = repo_url.split('/')[-1]  # Assuming the repo name is the last part of the URL
    
    # Check if any analysis is currently in progress
    if os.listdir(in_progress_directory):
        return jsonify({"error": "An analysis is already in progress"}), 400
    
    # Logic to start a new analysis
    # You need to implement how to actually start an analysis here
    # Example: writing a new file in the in_progress directory
    in_progress_path = f"{in_progress_directory}/{repo_name}.json"
    with open(in_progress_path, 'w') as file:
        json.dump({"status": "in_progress", "repo_url": repo_url}, file)
    
    return jsonify({"message": "Analysis started successfully for " + repo_name}), 202

if __name__ == '__main__':
    app.run(debug=True)