import requests
import json

url = "http://127.0.0.1:8000/v1/users"

payload = {
    "first_name": "Test",
    "last_name": "User",
    "email": "testuser@example.com",
    "mobile_number": "1234567890",
    "password": "Password123",
    "address": {
        "street_address": "123 Test St",
        "city": "Test City",
        "state": "Test State",
        "postal_code": "12345",
        "country": "Test Country",
    },
}

headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
