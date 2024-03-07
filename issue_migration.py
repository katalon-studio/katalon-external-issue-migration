import apis
import utils
import os
from dotenv import load_dotenv

load_dotenv()

projectID = os.environ['projectID']
sourcePath = os.environ['sourcePath']
destinationPath = os.environ['destinationPath']
sourceRepoID = os.environ['sourceRepoID']
destinationRepoID = os.environ['destinationRepoID']

def getSourceTestCases():
    testCases = utils.filterTestCasesByRepo(projectID, sourcePath, sourceRepoID)
    print("Source Test Cases: ")
    print(testCases)
    return testCases

def getDestinationTestCases():
    testCases = utils.filterTestCasesByRepo(projectID, destinationPath, destinationRepoID)
    print("Destination Test Cases: ")
    print(testCases)
    return testCases

def replacePath(sourcePath, destinationPath, path):
    index = path.find(sourcePath)

    # Replace the first sourcePath
    if index != -1:
        return path[:index] + destinationPath + path[index + len(sourcePath):]
    return None

def findDestinationTestCase(sourceTestCase, destinationPath, sourcePath, testCases):
    for testCase in testCases:
        fullDestinationPath = replacePath(sourcePath, destinationPath, sourceTestCase["path"])
        if testCase["name"] == sourceTestCase["name"] and testCase["path"] == fullDestinationPath:
            return testCase
    return None

def updateExternalIssues():
    sourceTestCases = getSourceTestCases()
    destinationTestCases = getDestinationTestCases()
    
    for sourceTestCase in sourceTestCases:
        destinationTestCase = findDestinationTestCase(sourceTestCase, destinationPath, sourcePath, destinationTestCases)
        if destinationTestCase is not None:
            print("Start migrate from source Test Case: ", sourceTestCase)
            print("to Test Case: ", destinationTestCase)
            for issue in sourceTestCase.get('externalRequirementIssueID'):
                apis.updateExternalRequirements(issue, destinationTestCase.get('id'), projectID)
            for issue in sourceTestCase.get('externalXrayTestIssueID'):
                # Unlink Xray Test from source Test Cases
                apis.deleteExternalXrayTests(issue, sourceTestCase['id'], projectID)

                # Link Xray Test to destination Test Cases
                apis.updateExternalXrayTests(issue, destinationTestCase.get('id'), projectID)
    
    print("Process finished!")
    
    return {
        "status": "Process finished!"
    }
    
def main():
    updateExternalIssues()