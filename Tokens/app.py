import requests
import json
import os
import logging
from flask import Flask, jsonify

app = Flask(__name__)

TOKEN_FILE = "token.json"
API_URL = "https://fleettracker.pacificnational.com.au/api/v1/auth/freightWebTokenRenew"

logging.basicConfig(level=logging.INFO)

def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            try:
                data = json.load(f)
                return data.get("token")
            except json.JSONDecodeError:
                logging.error("❌ Failed to parse token.json")
                return None
    else:
        logging.error("❌ token.json not found.")
        return None

def save_token(new_token):
    with open(TOKEN_FILE, "w") as f:
        json.dump({"token": new_token}, f)

def refresh_token():
    current_token = load_token()
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
            save_token(new_token)
            return True
        except Exception as e:
            logging.error(f"❌ Failed to extract new token: {e}")
            logging.error(response.text)
            return False
    else:
        logging.error(f"❌ Token refresh failed ({response.status_code})")
        logging.error(response.text)
        return False

# Manual startup call to refresh token when the app loads
def startup_refresh():
    logging.info("App starting — attempting to refresh token...")
    refresh_token()

startup_refresh()

@app.route("/")
def index():
    return jsonify({"message": "Token refresh API running."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
