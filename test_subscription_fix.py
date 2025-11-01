#!/usr/bin/env python3
"""
Test script to verify subscription notifications work after the fix
"""
import requests
import json
import time
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

# Global variable to store received notifications
received_notifications = []

class NotificationHandler(BaseHTTPRequestHandler):
    """Simple HTTP server to receive notifications"""
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            notification = json.loads(post_data.decode('utf-8'))
            received_notifications.append(notification)
            print(f"\n✅ NOTIFICATION RECEIVED!")
            print(json.dumps(notification, indent=2))
        except Exception as e:
            print(f"Error parsing notification: {e}")
        
        # Send 200 OK response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status": "ok"}')
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def start_notification_listener(port=8888):
    """Start HTTP server to listen for notifications"""
    server = HTTPServer(('0.0.0.0', port), NotificationHandler)
    print(f"🎧 Notification listener started on port {port}")
    server.serve_forever()

# Mobius4 configuration
MOBIUS_URL = "http://localhost:7599/Mobius"
ADMIN_ORIGIN = "SM"
LISTENER_URL = "http://localhost:8888/notify"

def test_subscription_notification():
    """Test that subscription notifications work correctly"""
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json; ty=23",
        "X-M2M-RI": "test-sub-notify",
        "X-M2M-Origin": ADMIN_ORIGIN,
    }
    
    # Start notification listener in background
    listener_thread = Thread(target=start_notification_listener, args=(8888,), daemon=True)
    listener_thread.start()
    time.sleep(2)  # Wait for listener to start
    
    print("\n" + "="*80)
    print("TESTING SUBSCRIPTION NOTIFICATION FIX")
    print("="*80)
    
    # Step 1: Create subscription
    print("\n📝 Step 1: Creating subscription for AE-WM/WM01-0032-0001/Data container")
    subscription_data = {
        "m2m:sub": {
            "rn": "test-sub-notification",
            "nu": [LISTENER_URL],
            "nct": 1,  # All attributes
            "enc": {
                "net": ["3"]  # Create events (as string, like your subscription)
            }
        }
    }
    
    sub_url = f"{MOBIUS_URL}/AE-WM/WM01-0032-0001/Data"
    try:
        # Delete old subscription if exists
        requests.delete(
            f"{sub_url}/test-sub-notification",
            headers={**headers, "X-M2M-RI": "delete-old-sub"},
            timeout=5
        )
        time.sleep(1)
    except:
        pass
    
    response = requests.post(sub_url, headers=headers, json=subscription_data, timeout=5)
    print(f"Status: {response.status_code}")
    if response.status_code in [200, 201]:
        print("✅ Subscription created successfully")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Failed to create subscription: {response.text}")
        return
    
    # Step 2: Create a CIN to trigger notification
    print("\n📝 Step 2: Creating CIN to trigger notification")
    time.sleep(2)  # Wait for subscription to be ready
    
    cin_data = {
        "m2m:cin": {
            "con": "['50', 'test-notification', 'TEST-001', 'location-test', 'violation-test']",
            "lbl": ["polluters_count", "bindata", "vehicle_number", "lct", "violations"]
        }
    }
    
    cin_headers = {
        **headers,
        "Content-Type": "application/json; ty=4",
        "X-M2M-RI": "test-cin-create"
    }
    
    response = requests.post(sub_url, headers=cin_headers, json=cin_data, timeout=5)
    print(f"Status: {response.status_code}")
    if response.status_code in [200, 201]:
        print("✅ CIN created successfully")
    else:
        print(f"❌ Failed to create CIN: {response.text}")
        return
    
    # Step 3: Wait and check for notification
    print("\n📝 Step 3: Waiting for notification...")
    time.sleep(3)
    
    print("\n" + "="*80)
    print("RESULTS")
    print("="*80)
    
    if len(received_notifications) > 0:
        print(f"✅ SUCCESS! Received {len(received_notifications)} notification(s)")
        for i, notif in enumerate(received_notifications, 1):
            print(f"\nNotification #{i}:")
            print(json.dumps(notif, indent=2))
    else:
        print("❌ FAILED! No notifications received")
        print("\nTroubleshooting:")
        print("1. Check Mobius4 logs: tail -f mobius4.log")
        print("2. Verify subscription exists: curl -X GET '" + sub_url + "/test-sub-notification' -H 'X-M2M-Origin: SM' -H 'Accept: application/json'")
        print("3. Check if listener URL is accessible from Mobius4")
    
    # Cleanup
    print("\n📝 Cleanup: Deleting test subscription")
    try:
        requests.delete(
            f"{sub_url}/test-sub-notification",
            headers={**headers, "X-M2M-RI": "cleanup-sub"},
            timeout=5
        )
        print("✅ Cleanup complete")
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")

if __name__ == "__main__":
    test_subscription_notification()
