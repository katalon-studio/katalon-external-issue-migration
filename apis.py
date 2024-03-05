import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()

username = os.environ['username']
apiKey = os.environ['apiKey']
hostURL = os.environ['hostURL']
sourceRepoID = os.environ['sourceRepoID']

# Search API just support max pageSize 300, need search recursively to get all record
def searchRecursively(currentPageIndex, searchParams, items) :
    headers = {
        'Content-Type': 'application/json'
    }
    searchParams["pagination"]["page"] = currentPageIndex
    response = requests.post(f"{hostURL}/api/v1/search", headers=headers, auth=HTTPBasicAuth(username, apiKey), json=searchParams).json()
    if (len(response["content"]) == 0) :
        return items

    items = items + response["content"]
    return searchRecursively(currentPageIndex + 1, searchParams, items)

def getTestCasesByPath(projectID, path, repoID):
    headers = {
        'Content-Type': 'application/json'
    }
    print(hostURL, username, projectID, apiKey, repoID != '')

    conditions = [
        # Get test object by project ID (required)
         {
            "key": "Project.id",
            "operator": "=",
            "value": f"{projectID}"
         },
         # Get test object by path (required)
         {
            "key": "path",
            "operator": "starts with",
            "value": f"{path}"
         }
    ]

    if (repoID != '') :
        # Get test object by ID (required)
        conditions.append({
            "key": "TestProject.id",
            "operator": "=",
            "value": f"{repoID}"
        })
    
    data = {
        "type": "TestCase",
        "conditions": conditions,
        "pagination": {
            "page": 0,
            "size": 300,
            # Short list of test object by a field
            "sorts": [
                "id, asc"
            ]
        }
    }

    return searchRecursively(0, data, [])

def getExternalRequirements(projectID, testCaseID):
    headers = {
        'Content-Type': 'application/json'
    }
    
    data = {
        "type": "ExternalRequirement",
        "conditions": [
            # Get test object by project ID (required)
            {
                "key": "Project.id",
                "operator": "=",
                "value": f"{projectID}"
            },
            # Get test object by test case ID (required)
            {
                "key": "TestCase.id",
                "operator": "=",
                "value": f"{testCaseID}"
            }
        ],
        "pagination": {
            "page": 0,
            "size": 300,
            # Short list of test object by a field
            "sorts": [
                "id, asc"
            ]
        }
    }

    return searchRecursively(0, data, [])

def getExternalXrayTests(projectID, testCaseID):
    headers = {
        'Content-Type': 'application/json'
    }
    
    data = {
        "type": "ExternalXrayTest",
        "conditions": [
            # Get test object by project ID (required)
            {
                "key": "Project.id",
                "operator": "=",
                "value": f"{projectID}"
            },
            # Get test object by test case ID (required)
            {
                "key": "TestCase.id",
                "operator": "=",
                "value": f"{testCaseID}"
            }
        ],
        "pagination": {
            "page": 0,
            "size": 300,
            # Short list of test object by a field
            "sorts": [
                "id, asc"
            ]
        }
    }

    return searchRecursively(0, data, [])

def updateExternalRequirements(externalIssueID, objectID, projectID):
    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "issueId": f"{externalIssueID}",
        "objectType": "TEST_CASE",
        "objectId": f"{objectID}"
    }

    response = requests.post(f"{hostURL}/api/v1/external-issue?projectId=" + f"{projectID}", headers=headers, auth=HTTPBasicAuth(username, apiKey), json=data).json()

    return response

def updateExternalXrayTests(externalIssueID, objectID, projectID):
    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "issueId": f"{externalIssueID}",
        "objectType": "XRAY_TEST_CASE",
        "objectId": f"{objectID}"
    }

    response = requests.post(f"{hostURL}/api/v1/external-issue?projectId=" + f"{projectID}", headers=headers, auth=HTTPBasicAuth(username, apiKey), json=data).json()

    return response

def deleteExternalRequirements(externalIssueID, objectID, projectID):
    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "issueId": f"{externalIssueID}",
        "objectType": "TEST_CASE",
        "objectId": f"{objectID}"
    }

    response = requests.delete(f"{hostURL}/api/v1/external-issue?projectId=" + f"{projectID}", headers=headers, auth=HTTPBasicAuth(username, apiKey), json=data).json()

    return response

def deleteExternalXrayTests(externalIssueID, objectID, projectID):
    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "issueId": f"{externalIssueID}",
        "objectType": "XRAY_TEST_CASE",
        "objectId": f"{objectID}"
    }

    response = requests.delete(f"{hostURL}/api/v1/external-issue?projectId=" + f"{projectID}", headers=headers, auth=HTTPBasicAuth(username, apiKey), json=data).json()

    return response