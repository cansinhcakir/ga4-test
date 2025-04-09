import requests
import json
import re
from googleapiclient.discovery import build
from google.oauth2 import service_account

measurement_id_mapping = {
    "bethand": "G-1111",
    "esfera": "G-2222",
    "betofcourse": "G-3333",
    "gizabet" : "G-6666",
    "redwin" : "G-12312"
}

url = "https://url2bet.com/js/domainList.js?v=1"
local_filename = "domainList.js"

response = requests.get(url)
if response.status_code == 200:
    with open(local_filename, "wb") as f:
        f.write(response.content)
else:
    print(f"{response.status_code}")

with open(local_filename, "r", encoding="utf-8") as file:
    js_content = file.read()

match = re.search(r"var domainList\s*=\s*{([\s\S]+?)};", js_content)
if match:
    js_dict_content = match.group(1)
    url_mapping = {}

    for line in js_dict_content.splitlines():
        line = line.strip().rstrip(",")
        if line:
            key_value = re.match(r'"(.+?)":\s*"(.+?)"', line)
            if key_value:
                key, value = key_value.groups()
                url_mapping[key] = value
else:
    url_mapping = {}

new_mapping = {url_mapping[key]: value for key, value in measurement_id_mapping.items() if key in url_mapping}

print(new_mapping)

SERVICE_ACCOUNT_FILE = '/Users/cans/Documents/pg-gtm-api-8ed197642948.json'
ACCOUNT_ID = "6273965368"
CONTAINER_ID = '209004377'
WORKSPACE_ID = '3'
VARIABLE_ID = '4'

def update_list(map_list, new_mapping):
    new_list = []
    for website, code in new_mapping.items():
        temp_list = []
        for item in map_list:
            new_map = []
            for template in item['map']:
                new_template = template.copy()
                if new_template['key'] == 'key':
                    new_template['value'] = website
                elif new_template['key'] == 'value':
                    new_template['value'] = code
                new_map.append(new_template)
            temp_list.append({'type': 'map', 'map': new_map})
        new_list.append(temp_list[0])

    return new_list


def update_lookup_table(new_map):

    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
    tagmanager = build('tagmanager', 'v2', credentials=creds)

    try:
        variable = tagmanager.accounts().containers().workspaces().variables().get(
            path=f'accounts/{ACCOUNT_ID}/containers/{CONTAINER_ID}/workspaces/{WORKSPACE_ID}/variables/{VARIABLE_ID}'
        ).execute()
    except Exception as e:
        print(e)
        return

    for param in variable["parameter"]:
        if param["type"] == "list":
            print(param["list"])
            param["list"] = update_list(param["list"], new_map)

    path = f'accounts/{ACCOUNT_ID}/containers/{CONTAINER_ID}/workspaces/{WORKSPACE_ID}/variables/{VARIABLE_ID}'

    try:
        updated_variable = tagmanager.accounts().containers().workspaces().variables().update(
            path=path,
            body=variable
        ).execute()
        
    except Exception as e:
        print(e)


if __name__ == '__main__':
    update_lookup_table(new_mapping)
  
