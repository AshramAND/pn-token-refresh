import requests
import json
import os

TOKEN_FILE = "token.json"
API_URL = "https://fleettracker.pacificnational.com.au/api/v1/auth/freightWebTokenRenew"

def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            try:
                data = json.load(f)
                return data.get("token")
            except json.JSONDecodeError:
                print("❌ Failed to parse token.json")
                return None
    else:
        print("❌ token.json not found.")
        return None

def save_token(new_token):
    with open(TOKEN_FILE, "w") as f:
        json.dump({"token": new_token}, f)

def refresh_token(current_token):
    headers = {
        "Authorization": f"Bearer {current_token}",
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.post(API_URL, headers=headers)
    if response.status_code == 200:
        try:
            new_token = response.json()["token"]
            print("✅ Token refreshed.")
            save_token(new_token)
        except Exception as e:
            print("❌ Failed to extract new token:", e)
            print(response.text)
    else:
        print(f"❌ Token refresh failed ({response.status_code})")
        print(response.text)

if __name__ == "__main__":
    current_token = load_token()
    if not current_token:
        print("⚠️ No token available to refresh. Exiting.")
        exit(1)
    refresh_token(current_token)
