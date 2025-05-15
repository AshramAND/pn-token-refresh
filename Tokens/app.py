from flask import Flask, jsonify
import json
import os
import requests

app = Flask(__name__)

TOKEN_FILE = os.path.join(os.path.dirname(__file__), "token.json")
API_URL = "https://fleettracker.pacificnational.com.au/api/v1/auth/freightWebTokenRenew"

def load_current_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            try:
                data = json.load(f)
                return data.get("token")
            except json.JSONDecodeError:
                return None
    return None

def save_new_token(new_token):
    with open(TOKEN_FILE, "w") as f:
        json.dump({"token": new_token}, f)

@app.route("/")
def home():
    return jsonify({"status": "API is running"}), 200

@app.route("/refresh", methods=["POST"])
def refresh_token():
    current_token = load_current_token()
    if not current_token:
        return jsonify({"error": "No token found"}), 400

    headers = {
        "Authorization": f"Bearer {current_token}",
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.post(API_URL, headers=headers)
    if response.status_code == 200:
        try:
            new_token = response.json()["token"]
            save_new_token(new_token)
            return jsonify({"status": "Token refreshed", "token": new_token}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to parse new token: {str(e)}"}), 500
    else:
        return jsonify({"error": "Token refresh failed", "code": response.status_code}), response.status_code
