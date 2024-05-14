# DevInsight User Manual

## 1. Introduction
Welcome to DevInsight, a comprehensive analytics tool designed to enhance the visibility of developer contributions in software projects using data from GitHub repositories. This manual will guide you through accessing, setting up, and navigating the application to leverage its full potential.

## 2. Accessing DevInsight
To start using DevInsight, you need to first clone the repository to your local machine.

**Step 1:** Navigate to the DevInsight GitHub Repository.  
**Step 2:** Copy the repository's URL by clicking on the 'Clone or download' button.  
**Step 3:** Open your terminal and run the following command:
```bash
git clone https://github.com/Emruur/CS453Project
```
## 3. Setting Up and Running the Backend (Flask)
### 3.1. Environment Setup:
Ensure Python and Flask are installed. You can install Flask using pip if it's not already installed:
```bash
pip install Flask
```
Set up config.py file in your the project under the “backend/src” directory with the necessary configuration for the GitHub API key, follow these steps:
#### 3.3.1. Navigate to the backend/src directory of the project:
```bash
cd CS453Project/backend/src
```
#### 3.3.2. Create config.py within this directory.
#### 3.3.3. Open config.py in your preferred text editor or IDE.
#### 3.3.4. In the config.py file, you need to define a variable to store the GitHub API key. Write the following line in the file, replace "your_api_key" with the actual API key you obtained from GitHub:
```bash
GITHUB_KEY = "your_api_key"
```
Ensure you keep this key secure and do not share it publicly. After entering the necessary code, save the file and close the text editor.
### 3.2. Running the Backend:
Navigate to the directory containing your Flask application, which is:
from GitHub:
```bash
cd CS453Project/backend
```
Run application with following command:
```bash
python backend.py
```
By default, Flask runs on http://localhost:5000. Ensure it’s running on this port, or adjust your frontend configuration accordingly if using a different port.
## 4. Setting Up and Running the Frontend (Next.js)
### 4.1. Environment Setup:
Ensure Node.js and npm (or Yarn) are installed.
Navigate to your Next.js application directory and install dependencies:
```bash
cd CS453Project/fronten/frontend
npm install
```
### 4.2.  Running the Frontend:
Start your Next.js application by running:
```bash
npm run dev
```
Next.js typically runs on http://localhost:3000. Open this URL in a web browser to view your application.
## 5. Basic Navigation 
### Homepage
Overview: The homepage displays a grid of tiles representing different GitHub repositories you are monitoring or can monitor.

#### Adding a Repository: Click on the "+" tile to add a new repository.
A dialog box appears prompting you to enter the URL of the GitHub repository.
After entering the URL, click “Add Repository” to integrate it into DevInsight.
#### Handling Common Issues During Repository Addition:
**Scenario 1:** Analysis Already in Progress:
If an analysis is currently running or the system is processing another repository, you may see a message stating, “An analysis is already in progress.”
Action: Wait until the current analysis is complete before attempting to add a new repository. This ensures system resources are not overburdened.

**Scenario 2:** Empty Repository URL:
If you attempt to add a repository without entering a URL, an error message “Repository URL is required” will be displayed.
Action: Ensure that you enter a valid GitHub repository URL into the input field before clicking “Add Repository.”

**Scenario 3:** Invalid or Inaccessible Repository URL:
Should you enter an incorrect URL or one that the system cannot access, an error message such as “Invalid URL” or “Repository not accessible” might appear.
Action: Verify the repository URL for any typos or errors, ensure you have the correct access permissions, and try again.

#### Repository Loading and Processing:
After adding a repository, you may observe a loading state, represented by a spinning icon on a repository tile. This indicates that the repository data is being fetched and processed.

Patience During Load: Repository analysis can take some time depending on the size of the repository and the complexity of the data. Patience during this phase is key.



