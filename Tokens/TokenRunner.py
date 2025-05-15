import os
import json
import time
import requests

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TOKEN_PATH = os.path.join(BASE_DIR, "token.json")

def load_token():
    try:
        with open(TOKEN_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ token.json not found.")
        return None

def save_token(token_data):
    with open(TOKEN_PATH, "w") as f:
        json.dump(token_data, f, indent=4)

def refresh_token(current_token):
    API_URL = "https://fleettracker.pacificnational.com.au/api/v1/auth/freightWebTokenRenew"
    headers = {
        "Authorization": f"Bearer {current_token['token']}"
    }
    response = requests.post(API_URL, headers=headers)
    if response.status_code == 200:
        new_token = response.json()
        save_token(new_token)
        print("Token updated!")
    else:
        print(f"Failed to refresh token: {response.status_code} {response.text}")

def main():
    current_token = load_token()
    if not current_token:
        print("⚠️ No token available to refresh. Exiting.")
        return
    
    while True:
        print("Refreshing token...")
        refresh_token(current_token)
        print("Sleeping for 1 hour...")
        time.sleep(3600)

if __name__ == "__main__":
    main()
