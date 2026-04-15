#!/usr/bin/env python3
import os, json, urllib.request, urllib.error

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
webhook = ""
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line.startswith("DISCORD_WEBHOOK="):
            webhook = line.split("=", 1)[1].strip()

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}
payload = json.dumps({"content": "test"}).encode()

# Test with ?wait=true
print("--- POST with ?wait=true ---")
url = f"{webhook}?wait=true"
print(f"URL: {url[:80]}...")
req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        body = r.read().decode()
        print(f"Status: {r.status}")
        print(f"Body  : {body[:300]}")
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.reason} — {e.read().decode()}")
except Exception as e:
    print(f"Error: {e}")
