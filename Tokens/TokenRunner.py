import os
import json
import subprocess
import requests

# === CONFIGURATION ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(BASE_DIR, "token.json")
API_URL = "https://fleettracker.pacificnational.com.au/api/v1/auth/freightWebTokenRenew"

# === TOKEN FUNCTIONS ===
def load_token():
    try:
        with open(TOKEN_PATH, "r") as f:
            token = json.load(f)
            print("📦 Loaded token from file.", flush=True)
            return token
    except FileNotFoundError:
        print("❌ token.json not found.", flush=True)
        return None

def save_token(token_data):
    with open(TOKEN_PATH, "w") as f:
        json.dump(token_data, f, indent=4)
    print("💾 Token saved to file.", flush=True)

def refresh_token(current_token):
    print("🔁 Attempting to refresh token...", flush=True)
    headers = {
        "Authorization": f"Bearer {current_token['token']}",
        "Content-Type": "application/json"
    }
    payload = {
        "token": current_token['token']
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            new_token = response.json()
            print("✅ Token successfully refreshed.", flush=True)
            save_token(new_token)
            return new_token
        else:
            print(f"❌ Failed to refresh token: {response.status_code} {response.text}", flush=True)
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}", flush=True)
        return None

# === GIT FUNCTIONS ===
def push_token_to_github():
    try:
        repo_root = os.path.abspath(os.path.join(BASE_DIR, ".."))
        subprocess.run(["git", "add", "."], cwd=repo_root, check=True)

        subprocess.run(
            ["git", "commit", "-m", "Auto-update token [skip ci]"],
            cwd=repo_root,
            check=False  # Allow no changes without crashing
        )

        subprocess.run(["git", "push", "--force"], cwd=repo_root, check=True)

        print("✅ Token force pushed to GitHub.", flush=True)

    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git push failed: {e}", flush=True)

# === MAIN SCRIPT ENTRY ===
def main():
    print("🚀 Token refresh script started", flush=True)

    current_token = load_token()
    if not current_token:
        print("⚠️ No token available to refresh. Exiting.", flush=True)
        return

    new_token = refresh_token(current_token)
    if new_token:
        push_token_to_github()
    else:
        print("⚠️ Using old token due to refresh failure.", flush=True)

    print("✅ Script completed.\n", flush=True)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"💥 Fatal error: {e}", flush=True)
