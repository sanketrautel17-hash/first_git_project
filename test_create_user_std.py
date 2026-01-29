import urllib.request
import json

url = "http://127.0.0.1:8002/v1/users"

payload = {
    "first_name": "Test",
    "last_name": "User",
    "email": "testuserunique_v5@example.com",
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

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(
    url, data=data, headers={"Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req) as response:
        print(f"Status Code: {response.getcode()}")
        print(f"Response Body: {response.read().decode('utf-8')}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
    print(f"Error Body: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
