#This gets the authorization token for farmbot logins  and notify teams that it ran requeires teams token url to be set up
import json
import requests
from getpass import getpass
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def notify_teams(webhook_url, message):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "text": message
    }
    response = requests.post(webhook_url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Teams notification sent successfully.")
    else:
        print(f"Failed to send notification to Teams. Status code: {response.status_code}")

# Inputs
SERVER = 'https://my.farm.bot'
EMAIL = input('FarmBot Web App account login email: ')
PASSWORD = getpass('FarmBot Web App account login password: ')

# Get your FarmBot authorization token
headers = {'content-type': 'application/json'}
user = {'user': {'email': EMAIL, 'password': PASSWORD}}
response = requests.post(f'{SERVER}/api/tokens', headers=headers, json=user, verify=False)

if response.status_code == 200:
    TOKEN = response.json()
    # Print the token
    print(f'{TOKEN = }')

    # Save the token to a local .json file
    with open('farmbot_authorization_token.json', 'w') as token_file:
        json.dump(TOKEN, token_file, indent=4)

    print("Token saved to farmbot_authorization_token.json")

    # Microsoft Teams webhook URL
    TEAMS_WEBHOOK_URL = 'https://outlook.office.com/webhook/YOUR_TEAMS_WEBHOOK_URL'

    # Notify Teams
    notify_teams(TEAMS_WEBHOOK_URL, "JSON file saved to local directory: farmbot_authorization_token.json")
else:
    print(f"Failed to get authorization token. Status code: {response.status_code}, Response: {response.text}")
