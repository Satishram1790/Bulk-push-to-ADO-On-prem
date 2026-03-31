# configure the neccassary Lib
import requests
from requests.auth import HTTPBasicAuth
import json
import creds
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import base64
import sys
import pandas as pd

# Define the project details                
Collection = f"{creds.DefaultCol}"
project_name = f"{creds.project}"
tfs_url = f"{creds.Org_URL}"

# User
user_identity = f"{creds.Users}" 

# workitem Type
workItemsType=f"{creds.WIT_Epic}"
AreaPath=f"{creds.Area}"
IterationPath=f"{project_name}\\{creds.Iteration}"

# Secure PAT
auth = f"{creds.PAT}"
token = base64.b64encode(f":{auth}".encode()).decode()

# # ADO REST API Version
API_VERSION = "7.1-preview.3"


# List of work items to create (excel format)
excel_file="Pipeline.xlsx"
df=pd.read_excel(excel_file,sheet_name='S7')
work_items_data = df.to_dict(orient="records")

# Base URL for Azure DevOps Work Item API
BASE_URL = f"{tfs_url}/{Collection}/{project_name}/_apis/wit/workitems"

# calling a Function to Create
try:
    # Import the create function from cred
    from creds import create_work_item
    # call the function
    create=create_work_item('work_item')

except ImportError:
    print("Error: Could not import the function from creds")
# except ValueError as ve:
#     print(f"Value Error: {ve}")
# except Exception as e:
#     print(f"Unexpected error: {e}")


# Bulk creation loop
for item in work_items_data:
    #print(item)
    create_work_item(item)
# Exit the loop
sys.exit()
