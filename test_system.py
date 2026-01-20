import requests
import json
import sys

# Test Data
TEST_PAYLOAD = {
    "decision_text": "I want to invest my entire savings into a new crypto coin because my friend said it will go up 100x next week.",
    "domain": "finance",
    "time_horizon": "short",
    "values": ["security", "long-term growth"]
}

def test_audit():
    print("Testing SecondBrain OS Audit Endpoint...")
    url = "http://localhost:8000/audit"
    
    try:
        response = requests.post(url, json=TEST_PAYLOAD)
        
        if response.status_code == 200:
            print("[OK] Success! API responded with 200 OK.")
            data = response.json()
            
            # Check for banned phrases
            json_str = json.dumps(data).lower()
            banned = ["you should", "i recommend", "best option is"]
            found_banned = [phrase for phrase in banned if phrase in json_str]
            
            if found_banned:
                print(f"[FAIL] CONSTRAINT VIOLATION: Found banned phrases: {found_banned}")
            else:
                print("[OK] Constraint Check Passed: No advice phrases found.")
                
            print(f"Risk Score: {data.get('risk_score')}")
            print(f"Bias Score: {data.get('bias_score')}")
            print(f"Alignment Score: {data.get('alignment_score')}")
            
        else:
            print(f"[FAIL] Failed: Status Code {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("[FAIL] Connection Error: Is the backend running? (uvicorn backend.main:app)")

if __name__ == "__main__":
    test_audit()
