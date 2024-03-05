# Katalon external issue migration

### Overview
This Python script offers the ability to migrate external issues, such as requirements and Xray tests, from test cases in one script repository to another based on the test case name.

Technically, the script utilizes the public APIs of Katalon, which can retrieve test cases and external issues, then update the relationship between test cases and external issues as needed.

**Note**
- This app is written on Python 3.9.
- Page size of `Get Test Case` endpoint is 300.
- Provided data will not be stored.

### Usage
1. Creating a .env file with the below params

    - `username`: Your username that is used in Katalon
    - `apiKey`: Your valid API key that is created in Katalon
    - `hostURL`: Your Katalon server
    - `projectID`: Your Katalon project ID
    - `sourcePath`: The directory of test cases in your legacy repository
    - `destinationPath`: The directory of test cases in your current repository
    - `sourceRepoID`: Your legacy repository ID (Leave this param blank if your source repository is Uploaded Data folder)
    - `destinationRepoID`: Your current repository ID (Leave this param blank if your destination repository is Uploaded Data folder)

2. (Optional) Set up your vitural environment
    > python3 -m venv venv

    > source venv/bin/activate

3. Install dependencies
    > pip3 install -r requirements.txt

4. Trigger the script
    > python3 main.py
