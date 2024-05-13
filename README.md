# DevInsight User Manual

## User Manual

### 1. Introduction
Welcome to DevInsight, a comprehensive analytics tool designed to enhance the visibility of developer contributions in software projects using data from GitHub repositories. This manual will guide you through accessing, setting up, and navigating the application to leverage its full potential.

### 2. Accessing DevInsight
To start using DevInsight, you need to first clone the repository to your local machine.

**Step 1:** Navigate to the DevInsight GitHub Repository.  
**Step 2:** Copy the repository's URL by clicking on the 'Clone or download' button.  
**Step 3:** Open your terminal and run the following command:
```bash
git clone https://github.com/Emruur/CS453Project
```
### 3. Setting Up and Running the Backend (Flask)
####1. Environment Setup:
**Ensure Python and Flask are installed. You can install Flask using pip if it's not already installed:
```bash
pip install Flask
```
**Set up config.py file in your the project under the “backend/src” directory with the necessary configuration for the GitHub API key, follow these steps:
1. Navigate to the backend/src directory of the project:
```bash
cd CS453Project/backend/src
```
2. Create config.py within this directory.
3. Open config.py in your preferred text editor or IDE.
4. In the config.py file, you need to define a variable to store the GitHub API key. Write the following line in the file, replace "your_api_key" with the actual API key you obtained from GitHub:
```bash
GITHUB_KEY = "your_api_key"
```
Ensure you keep this key secure and do not share it publicly. After entering the necessary code, save the file and close the text editor.
####2. Running the Backend:
