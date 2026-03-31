import pandas as pd
import creds
import requests
from requests.auth import HTTPBasicAuth
import json
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# from tabulate import tabulate

# Configure
Collection = "BDS"
project_name = "OKC_PST_Team"

# PAT
auth = HTTPBasicAuth("", creds.PAT)

# ADO REST API
url_base = f"{creds.Org_URL}"

headers = {
    "Content-Type": "application/json"
}

# Payload via WIQL query
wiql_query = {
    "query":
        "SELECT [System.Id],[System.Title],[System.State],[System.AssignedTo],[System.Description],[Microsoft.VSTS.Scheduling.StoryPoints] FROM WorkItems WHERE [System.WorkItemType] = 'User Story' AND [System.TeamProject] = 'OKC_PST_Team' ORDER BY [Microsoft.VSTS.Scheduling.StoryPoints] ASC"
}


# Execute WIQL query Payload
wiql_url = f"{url_base}/{Collection}/{project_name}/_apis/wit/wiql?api-version=7.1"

response = requests.post(wiql_url, auth=HTTPBasicAuth("",creds.PAT),headers=headers,json=wiql_query,verify=False)

if response.status_code !=200:
    raise Exception(f"Error querying work items:{response.status_code} {response.text}")

# Read the response file now
WII=[item['id'] for item in response.json()['workItems']]

# Function to split IDs into chunks of 200
def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# Fetch details in batches
all_details = []
batch_url = f"{url_base}/{Collection}/{project_name}/_apis/wit/workitemsbatch?api-version=7.1"

for id_chunk in chunk_list(WII[:10], 2):
    payload = {
        "ids": id_chunk,
        "fields": ["System.Id", "System.Title","System.State","System.AssignedTo","System.Description","Microsoft.VSTS.Scheduling.StoryPoints"] # List of fields you want
    }
    
    # Use POST instead of GET for the batch endpoint
    batch_response = requests.post(
        batch_url, 
        auth=HTTPBasicAuth("", creds.PAT),
        headers=headers, 
        json=payload, 
        verify=False
    )
    # print(payload)
    # print(batch_response.status_code)
    # sys.exit
    if batch_response.status_code == 200:
        all_details.extend(batch_response.json()['value'])
    else:
        print(batch_response.status_code,batch_response.text)

# View your data

# Convert all_details into a structured list of dicts
records = []
for item in all_details:
    fields = item['fields']
    assigned = fields.get('System.AssignedTo', {})
    assigned_name = assigned.get('displayName', 'Unassigned')
    description = fields.get('System.Description', 'No Description')

    records.append({
        "ID": item['id'],
        "Title": fields.get('System.Title'),
        "Status": fields.get('System.State'),
        "StoryPoints": fields.get('Microsoft.VSTS.Scheduling.StoryPoints'),
        "AssignedTo": assigned_name,
        "Description": description
    })

# Create DataFrame
df = pd.DataFrame(records)

# Save to CSV
df.to_csv("workitems_output.csv", index=False)

print("Work item details saved to workitems_output.csv")

# for item in all_details:
#     fields = item['fields']
#     assigned = fields.get('System.AssignedTo', {})
#     assigned_name = assigned.get('displayName', 'Unassigned')
#     description=fields.get(str('System.Description'),'No Decription')
    

#     print(f"""
# ID: {item['id']}
# Title: {fields.get('System.Title')}
# Status: {fields.get('System.State')}
# StoryPoints: {fields.get('Microsoft.VSTS.Scheduling.StoryPoints')}
# AssignedTo: {assigned_name}
# Description:{description}
# """)
    
sys.exit()