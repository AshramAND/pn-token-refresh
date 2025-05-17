import json
import requests
import os
from datetime import datetime

TOKEN_FILE = os.path.join(os.path.dirname(__file__), 'token.json')
API_URL = "https://fleettracker.pacificnational.com.au/api/v1/auth/freightWebTokenRenew"

def load_token():
    with open(TOKEN_FILE, 'r') as f:
        data = json.load(f)
    print("📦 Loaded token from file.")
    return data['token']

def save_token(new_token):
    # The API returns an object with token string + metadata,
    # save it back as a full JSON to the token file
    with open(TOKEN_FILE, 'w') as f:
        json.dump(new_token, f, indent=2)
    print("💾 Saved new token to file.")

def refresh_token(old_token):
    headers = {
        "Authorization": f"Bearer {old_token}",
        "Content-Type": "application/json"
    }
    # Payload is JSON with just the token string, no other fields
    payload = {
        "token": old_token
    }
    print("🔁 Attempting to refresh token...")
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        new_token_json = response.json()
        print(f"✅ Token refreshed successfully at {datetime.now()}")
        return new_token_json
    except requests.RequestException as e:
        print(f"❌ Connection error or bad response: {e}")
        return None

def main():
    print("🚀 Token refresh script started")
    old_token = load_token()
    new_token = refresh_token(old_token)

    if new_token and 'token' in new_token:
        save_token(new_token)
    else:
        print("⚠️ Using old token due to refresh failure.")

    print("✅ Script completed.")

if __name__ == "__main__":
    main()
