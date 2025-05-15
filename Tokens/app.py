from flask import Flask
import requests
import json
import os
import logging
import time

app = Flask(__name__)

TOKEN_FILE = "/Users/hugo/Desktop/Full/Tokens/token.json"
API_URL = "https://fleettracker.pacificnational.com.au/api/v1/auth/freightWebTokenRenew"

logging.basicConfig(level=logging.INFO)

def refresh_token():
    if not os.path.exists(TOKEN_FILE):
        logging.error("❌ token.json not found.")
        return False

    with open(TOKEN_FILE, "r") as f:
        try:
            data = json.load(f)
            current_token = data.get("token")
        except json.JSONDecodeError:
            logging.error("❌ Failed to parse token.json")
            return False

    if not current_token:
        logging.warning("⚠️ No token available to refresh.")
        return False

    headers = {
        "Authorization": f"Bearer {current_token}",
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.post(API_URL, headers=headers)

    if response.status_code == 200:
        try:
            new_token = response.json()["token"]
            logging.info("✅ Token refreshed.")

            with open(TOKEN_FILE, "w") as f:
                json.dump({"token": new_token}, f)
            return True

        except Exception as e:
            logging.error(f"❌ Failed to extract new token: {e}")
            logging.error(response.text)
            return False
    else:
        logging.error(f"❌ Token refresh failed ({response.status_code})")
        logging.error(response.text)
        return False

@app.before_first_request
def startup_refresh():
    logging.info("App started — attempting to refresh token...")
    refresh_token()

@app.route('/')
def index():
    return "Token Refresh Service is running."

@app.route('/status')
def status():
    if os.path.exists(TOKEN_FILE):
        last_modified = os.path.getmtime(TOKEN_FILE)
        return f"Token file last updated: {time.ctime(last_modified)}"
    else:
        return "Token file not found."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
