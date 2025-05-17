import socket
import requests
import json
import os
import sys

# --- DNS Monkeypatch to fix GitHub Actions DNS resolution ---

_real_getaddrinfo = socket.getaddrinfo

def custom_getaddrinfo(host, *args, **kwargs):
    if host == 'fleettracker.pacificnational.com.au':
        # Use the IP found from nslookup (203.21.182.25)
        return _real_getaddrinfo('203.21.182.25', *args, **kwargs)
    return _real_getaddrinfo(host, *args, **kwargs)

socket.getaddrinfo = custom_getaddrinfo

# --- Your existing token refresh code starts here ---

TOKEN_FILE = os.path.join(os.path.dirname(__file__), 'token.json')

API_URL = 'https://fleettracker.pacificnational.com.au/api/v1/auth/freightWebTokenRenew'

def load_token():
    try:
        with open(TOKEN_FILE, 'r') as f:
            print("📦 Loaded token from file.")
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load token file: {e}")
        sys.exit(1)

def save_token(token_data):
    try:
        with open(TOKEN_FILE, 'w') as f:
            json.dump(token_data, f, indent=4)
        print("💾 Token saved to file.")
    except Exception as e:
        print(f"❌ Failed to save token file: {e}")

def refresh_token(old_token):
    headers = {
        'Authorization': f'Bearer {old_token["token"]}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    print("🔁 Attempting to refresh token...")
    try:
        response = requests.post(API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if 'token' in data:
            print("✅ Token refreshed successfully.")
            return data
        else:
            print("❌ No token found in response.")
    except Exception as e:
        print(f"❌ Connection error or bad response: {e}")
    return None

def main():
    print("🚀 Token refresh script started")
    old_token = load_token()
    new_token = refresh_token(old_token)
    if new_token:
        save_token(new_token)
    else:
        print("⚠️ Using old token due to refresh failure.")
    print("✅ Script completed.")

if __name__ == '__main__':
    main()
