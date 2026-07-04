import requests
import time
import os
import sqlite3

# Try to get from DB
api_key = None
db_paths = ["database/storyboard.db", "storyboard.db"]
for db_path in db_paths:
    try:
        if not os.path.exists(db_path): continue
        print(f"Checking {db_path}...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]
        if "provider_configs" in tables:
            cursor.execute("SELECT api_key FROM provider_configs WHERE type='openrouter'")
            row = cursor.fetchone()
            if row and row[0]:
                api_key = row[0]
                print(f"Found API key in {db_path}")
                conn.close()
                break
        conn.close()
    except Exception as e:
        print(f"Error checking {db_path}: {e}")

if not api_key:
    print("No API Key found")
    exit(1)

headers = {
    "Authorization": f"Bearer {api_key}",
    "HTTP-Referer": "https://github.com/kirklasalle/storyboard",
    "X-Title": "Storyboard AI"
}

print(f"Benchmarking OpenRouter...")
start = time.time()
try:
    # Use the /auth/key endpoint for fast ping
    response = requests.get("https://openrouter.ai/api/v1/auth/key", headers=headers, timeout=10)
    print(f"Auth Key Check: {response.status_code} in {time.time() - start:.2f}s")
except Exception as e:
    print(f"Auth Key Check Failed: {e}")

start = time.time()
try:
    # List models
    response = requests.get("https://openrouter.ai/api/v1/models", headers=headers, timeout=10)
    print(f"Models List: {response.status_code} ({len(response.json()['data'])} models) in {time.time() - start:.2f}s")
except Exception as e:
    print(f"Models List Failed: {e}")
