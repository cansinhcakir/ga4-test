import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = "/Users/cans/Documents/pg-gtm-api-8ed197642948.json"
SCOPES = ["https://www.googleapis.com/auth/tagmanager.readonly"]

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build("tagmanager", "v2", credentials=credentials)

ACCOUNT_ID = "6273965368"
CONTAINER_ID = "209004377"
WORKSPACE_ID = "3"

def get_gtm_variables():
    request = service.accounts().containers().workspaces().variables().list(
        parent=f"accounts/{ACCOUNT_ID}/containers/{CONTAINER_ID}/workspaces/{WORKSPACE_ID}"
    )
    response = request.execute()

    if "variable" in response:
        for var in response["variable"]:
            print(f"ID: {var['variableId']}, Name: {var['name']}, Type: {var['type']}")
    else:
        print("No variables found.")


def list_gtm_accounts():
    request = service.accounts().list()
    response = request.execute()
    print(json.dumps(response, indent=4)) 
# list_gtm_accounts()

get_gtm_variables()