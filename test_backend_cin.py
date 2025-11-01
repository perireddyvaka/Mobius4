#!/usr/bin/env python3
import requests
import json

url = "http://127.0.0.1:8008/nodes/create-cin/1"
data = {
  "tds": "example"
}
headers = {"Content-Type": "application/json", "Authorization": "Bearer 4d0a2259bcdde9d8f6953812e5f1eb26"}

print("Testing CIN creation through your backend...")
print(f"URL: {url}")
print(f"Data: {json.dumps(data, indent=2)}")
print(f"Headers: {headers}")

try:
    response = requests.post(url, data=json.dumps(data), headers=headers, timeout=10)
    print(f"Response Status: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Body: {response.text}")
    
    if response.status_code == 200:
        print("Success:", response.text)
    else:
        print("Error:", response.status_code, response.text)
except Exception as e:
    print(f"Error: {e}")