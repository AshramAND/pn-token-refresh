import json
import requests
import sys

TOKEN_FILE = 'Tokens/token.json'  # Adjust path if needed
API_URL = 'https://fleettracker.pacificnational.com.au/api/v2/freightWebTokenRenew'

def load_token():
    try:
        with open(TOKEN_FILE, 'r') as f:
            token_data = json.load(f)
        print("📦 Loaded token from file.")
        return token_data
    except FileNotFoundError:
        print(f"❌ Token file not found: {TOKEN_FILE}")
    except json.JSONDecodeError:
        print(f"❌ Token file is not valid JSON: {TOKEN_FILE}")
    return None

def save_token(token_data):
    try:
        with open(TOKEN_FILE, 'w') as f:
            json.dump(token_data, f, indent=4)
        print("💾 Token saved to file.")
    except Exception as e:
        print(f"❌ Failed to save token file: {e}")

def refresh_token(old_token_data):
    if not old_token_data or 'token' not in old_token_data:
        print("❌ Invalid old token data, cannot refresh.")
        return None

    headers = {
        'Authorization': f"Bearer {old_token_data['token']}",
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    print("🔁 Attempting to refresh token...")
    try:
        response = requests.post(API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"📬 Response JSON: {data}")

        if 'token' in data:
            print("✅ Token refreshed successfully.")
            return data
        else:
            print("❌ No 'token' found in API response.")
            return None
    except requests.RequestException as e:
        print(f"❌ HTTP request failed: {e}")
        return None
    except json.JSONDecodeError:
        print("❌ Failed to parse JSON response.")
        return None

def main():
    print("🚀 Token refresh script started")
    old_token_data = load_token()
    if old_token_data is None:
        print("❌ Exiting: no valid token to refresh.")
        sys.exit(1)

    new_token_data = refresh_token(old_token_data)
    if new_token_data is None:
        print("⚠️ Token refresh failed, keeping old token.")
    else:
        old_token_str = old_token_data.get('token')
        new_token_str = new_token_data.get('token')
        print(f"🔍 Old token: {old_token_str}")
        print(f"🔍 New token: {new_token_str}")

        if old_token_str != new_token_str:
            print("✨ Token changed, saving new token.")
            save_token(new_token_data)
        else:
            print("⚠️ Token did not change, not saving.")

    print("✅ Script completed.")

if __name__ == "__main__":
    main()
