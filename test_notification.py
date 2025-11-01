#!/usr/bin/env python3
import requests
import json
import time

# Create a CIN to trigger notification
def create_cin():
    url = "http://localhost:7599/~/lmsb7lz7d1/3-20251031100851365535"
    headers = {
        "X-M2M-Origin": "SOrigin",
        "X-M2M-RI": f"cin-test-{int(time.time())}",
        "Content-Type": "application/json"
    }
    
    data = {
        "m2m:cin": {
            "con": "test notification content - " + str(int(time.time())),
            "rn": f"cin-test-noti-{int(time.time())}"
        }
    }
    
    print("Creating CIN to trigger notification...")
    print(f"URL: {url}")
    print(f"Headers: {headers}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_cin()