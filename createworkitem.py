
import requests
from requests.auth import HTTPBasicAuth
import json
import creds
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import base64
import sys
import pandas as pd
                
Collection = f"{creds.DefaultCol}"
project_name = f"{creds.project}"
tfs_url = f"{creds.Org_URL}"
# User
user_identity = f"{creds.Users}" 
# workitem Type

workItemsType=f"{creds.WIT_Epic}"
AreaPath=f"{creds.Area}"
IterationPath=f"{project_name}\\{creds.Iteration}"

# PAT
auth = f"{creds.PAT}"
token = base64.b64encode(f":{auth}".encode()).decode()

# # ADO REST API Version
API_VERSION = "7.1-preview.3"


# List of work items to create (excel format)
excel_file="Pipeline.xlsx"
df=pd.read_excel(excel_file,sheet_name='S6')
work_items_data = df.to_dict(orient="records")

# Base URL for Azure DevOps Work Item API
BASE_URL = f"{tfs_url}/{Collection}/{project_name}/_apis/wit/workitems"

# Headers required for JSON Patch
headers = {
    "Content-Type": "application/json-patch+json",
     "Authorization": f"Basic {token}"
}

def create_work_item(work_item):
    # Prepare JSON Patch document
    payload = [
        {"op": "add", "path": "/fields/System.Title", "value": work_item["Title"]},
        {"op": "add", "path": "/fields/System.Description", "value": work_item["Description"]},
        {"op": "add", "path": "/fields/System.AssignedTo","value": work_item["AssignedTo"]},
        {"op": "add", "path": "/fields/Microsoft.VSTS.Scheduling.StoryPoints", "value": work_item["StoryPoints"]},
        {"op": "add", "path": "/fields/System.AreaPath","value": work_item["AreaPath"]},
        {"op": "add", "path": "/fields/System.IterationPath","value": work_item["IterationPath"]}
    ]
    
    # Construct API endpoint for the specific work item type
    API_url = f"{BASE_URL}/${work_item['Type']}?api-version={API_VERSION}"
    response = requests.post(API_url, headers=headers, data=json.dumps(payload),verify=False)
    if response.status_code in [200, 201]:
        print(f"Successfully created {work_item['Type']}: {work_item['Title']} (ID: {response.json()['id']})")
    else:
        print(f"Failed to create {work_item['Title']}: {response.status_code} {response.text}")    

# Bulk creation loop
for item in work_items_data:
    #print(item)
    create_work_item(item)
    
sys.exit()