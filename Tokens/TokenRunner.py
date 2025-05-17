import os
import json
import time
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
            return json.load(f)
    except FileNotFoundError:
        print("❌ token.json not found.")
        return None

def save_token(token_data):
    with open(TOKEN_PATH, "w") as f:
        json.dump(token_data, f, indent=4)

def refresh_token(current_token):
    headers = {
        "Authorization": f"Bearer {current_token['token']}"
    }
    response = requests.post(API_URL, headers=headers)
    if response.status_code == 200:
        new_token = response.json()
        save_token(new_token)
        print("✅ Token updated!")
        return new_token  # return the new token
    else:
        print(f"❌ Failed to refresh token: {response.status_code} {response.text}")
        return None


# === GIT FUNCTIONS ===

def push_token_to_github():
    try:
        repo_root = os.path.abspath(os.path.join(BASE_DIR, ".."))

        subprocess.run(["git", "add", "."], cwd=repo_root, check=True)

        subprocess.run(
            ["git", "commit", "-m", "Auto-update token [skip ci]"],
            cwd=repo_root,
            check=False  # Allow empty commits
        )

        subprocess.run(["git", "push", "--force"], cwd=repo_root, check=True)

        print("✅ Token force pushed to GitHub.")

    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git push failed: {e}")

# === MAIN LOOP ===


def main():
    current_token = load_token()
    if not current_token:
        print("⚠️ No token available to refresh. Exiting.")
        return

    while True:
        print("🔁 Refreshing token...")
        new_token = refresh_token(current_token)
        if new_token:
            current_token = new_token  # update token in memory
            push_token_to_github()

        print("😴 Sleeping for 1 hour...")
        time.sleep(3600)
if __name__ == "__main__":
    main()