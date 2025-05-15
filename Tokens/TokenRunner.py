from flask import Flask, jsonify
import requests
import json
import os

app = Flask(__name__)

TOKEN_FILE = "token.json"
API_URL = "https://fleettracker.pacificnational.com.au/api/v1/auth/freightWebTokenRenew"

def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            try:
                data = json.load(f)
                return data.get("token")
            except json.JSONDecodeError:
                return None
    return None

def save_token(new_token):
    with open(TOKEN_FILE, "w") as f:
        json.dump({"token": new_token}, f)

def refresh_token():
    current_token = load_token()
    if not current_token:
        return {"error": "No current token to refresh"}, 400

    headers = {
        "Authorization": f"Bearer {current_token}",
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.post(API_URL, headers=headers)

    if response.status_code == 200:
        try:
            new_token = response.json()["token"]
            save_token(new_token)
            return {"message": "Token refreshed", "token": new_token}
        except Exception as e:
            return {"error": str(e)}, 500
    else:
        return {"error": f"Refresh failed ({response.status_code})"}, 500

@app.route("/refresh", methods=["GET"])
def refresh():
    return jsonify(refresh_token())

@app.route("/token", methods=["GET"])
def get_token():
    token = load_token()
    if token:
        return jsonify({"token": token})
    else:
        return jsonify({"error": "No token available"}), 404
