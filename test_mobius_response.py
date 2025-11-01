#!/usr/bin/env python3
"""
Test script to see the actual response structure from Mobius4
This will help identify the correct JSON path for parsing CINs
"""
import requests
import json
import sys

# Mobius4 configuration from default.json
MOBIUS_URL = "http://localhost:7599"  # Default HTTP port from config
MOBIUS_BASE = "Mobius"  # csebase_rn from config
ADMIN_ORIGIN = "SM"  # admin from config

def test_mobius_response(vertical_short_name, node_name, container_name="Data"):
    """
    Test different Mobius4 endpoints to see actual response structure
    
    Args:
        vertical_short_name: e.g., "WM", "EM", etc.
        node_name: your node name
        container_name: usually "Data"
    """
    
    print("=" * 80)
    print("TESTING MOBIUS4 RESPONSE STRUCTURES")
    print("=" * 80)
    
    headers = {
        "Accept": "application/json",
        "X-M2M-RI": "test-request-12345",
        "X-M2M-Origin": ADMIN_ORIGIN,
    }
    
    # Test 1: Get AE (Application Entity) - the node itself
    print("\n" + "=" * 80)
    print(f"TEST 1: GET AE (Node) - /{vertical_short_name}/{node_name}")
    print("=" * 80)
    url_ae = f"{MOBIUS_URL}/{MOBIUS_BASE}/{vertical_short_name}/{node_name}"
    print(f"URL: {url_ae}")
    
    try:
        response = requests.get(url_ae, headers=headers, timeout=5)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response JSON:")
            print(json.dumps(data, indent=2))
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Get Data Container (without rcn)
    print("\n" + "=" * 80)
    print(f"TEST 2: GET Data Container - /{vertical_short_name}/{node_name}/{container_name}")
    print("=" * 80)
    url_cnt = f"{MOBIUS_URL}/{MOBIUS_BASE}/{vertical_short_name}/{node_name}/{container_name}"
    print(f"URL: {url_cnt}")
    
    try:
        response = requests.get(url_cnt, headers=headers, timeout=5)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response JSON:")
            print(json.dumps(data, indent=2))
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Get Data Container with rcn=4 (attributes + child resources)
    print("\n" + "=" * 80)
    print(f"TEST 3: GET Data Container with rcn=4 - /{vertical_short_name}/{node_name}/{container_name}?rcn=4")
    print("=" * 80)
    url_rcn4 = f"{MOBIUS_URL}/{MOBIUS_BASE}/{vertical_short_name}/{node_name}/{container_name}?rcn=4"
    print(f"URL: {url_rcn4}")
    
    try:
        response = requests.get(url_rcn4, headers=headers, timeout=5)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response JSON:")
            print(json.dumps(data, indent=2))
            
            # Try to parse CINs
            print("\n" + "-" * 80)
            print("PARSING CINs:")
            print("-" * 80)
            
            # Method 1: Check for m2m:cnt -> m2m:cin
            if "m2m:cnt" in data and "m2m:cin" in data["m2m:cnt"]:
                cins = data["m2m:cnt"]["m2m:cin"]
                print(f"✓ Found CINs via path: m2m:cnt -> m2m:cin")
                print(f"  Number of CINs: {len(cins) if isinstance(cins, list) else 1}")
                if isinstance(cins, list) and len(cins) > 0:
                    print(f"  First CIN sample:")
                    print(json.dumps(cins[0], indent=4))
            
            # Method 2: Check for m2m:rsp -> m2m:cin (old method)
            elif "m2m:rsp" in data and "m2m:cin" in data["m2m:rsp"]:
                cins = data["m2m:rsp"]["m2m:cin"]
                print(f"✓ Found CINs via path: m2m:rsp -> m2m:cin")
                print(f"  Number of CINs: {len(cins) if isinstance(cins, list) else 1}")
            else:
                print(f"✗ No CINs found. Available keys:")
                print(f"  Top level: {list(data.keys())}")
                if "m2m:cnt" in data:
                    print(f"  Inside m2m:cnt: {list(data['m2m:cnt'].keys())}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 4: Get Latest CIN using /la
    print("\n" + "=" * 80)
    print(f"TEST 4: GET Latest CIN - /{vertical_short_name}/{node_name}/{container_name}/la")
    print("=" * 80)
    url_la = f"{MOBIUS_URL}/{MOBIUS_BASE}/{vertical_short_name}/{node_name}/{container_name}/la"
    print(f"URL: {url_la}")
    
    try:
        response = requests.get(url_la, headers=headers, timeout=5)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response JSON:")
            print(json.dumps(data, indent=2))
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 5: Try /latest (incorrect but let's see)
    print("\n" + "=" * 80)
    print(f"TEST 5: GET Latest CIN - /{vertical_short_name}/{node_name}/{container_name}/latest (WRONG)")
    print("=" * 80)
    url_latest = f"{MOBIUS_URL}/{MOBIUS_BASE}/{vertical_short_name}/{node_name}/{container_name}/latest"
    print(f"URL: {url_latest}")
    
    try:
        response = requests.get(url_latest, headers=headers, timeout=5)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response JSON:")
            print(json.dumps(data, indent=2))
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 80)
    print("TESTS COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python test_mobius_response.py <vertical_short_name> <node_name> [container_name]")
        print("\nExample:")
        print("  python test_mobius_response.py WM node001")
        print("  python test_mobius_response.py EM sensor_123 Data")
        print("\nPlease provide:")
        print("  - vertical_short_name: e.g., WM, EM, etc.")
        print("  - node_name: your node name")
        print("  - container_name (optional): default is 'Data'")
        sys.exit(1)
    
    vertical = sys.argv[1]
    node = sys.argv[2]
    container = sys.argv[3] if len(sys.argv) > 3 else "Data"
    
    test_mobius_response(vertical, node, container)
