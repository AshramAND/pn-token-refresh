import os
import json
import time
import requests
import json
import os

TOKEN_FILE = "/Users/hugo/Desktop/Full/Tokens/token.json"
API_URL = "https://fleettracker.pacificnational.com.au/api/v1/auth/freightWebTokenRenew"

# Load the last saved token
if os.path.exists(TOKEN_FILE):
    with open(TOKEN_FILE, "r") as f:
        try:
            data = json.load(f)
            current_token = data.get("token")
        except json.JSONDecodeError:
            print("❌ Failed to parse token.json")
            current_token = None
else:
    print("❌ token.json not found.")
    current_token = None

if not current_token:
    print("⚠️ No token available to refresh.")
    exit()

# Set headers with the current token
headers = {
    "Authorization": f"Bearer {current_token}",
    "User-Agent": "Mozilla/5.0"
}

# Make the refresh request
response = requests.post(API_URL, headers=headers)

if response.status_code == 200:
    try:
        new_token = response.json()["token"]
        print("✅ Token refreshed.")

        # Save new token to file
        with open(TOKEN_FILE, "w") as f:
            json.dump({"token": new_token}, f)

    except Exception as e:
        print("❌ Failed to extract new token:", e)
        print(response.text)
else:
    print(f"❌ Token refresh failed ({response.status_code})")
    print(response.text)