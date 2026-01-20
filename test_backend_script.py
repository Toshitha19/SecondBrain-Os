import requests
import json

url = "http://127.0.0.1:8000/audit"
payload = {
    "decision_text": "Should I move to a new city for a job?",
    "domain": "career",
    "time_horizon": "long",
    "values": ["career growth", "family", "adventure"]
}
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Response JSON:")
        print(json.dumps(response.json(), indent=2))
    else:
        print("Error Response:")
        print(response.text)
except Exception as e:
    print(f"Request failed: {e}")
