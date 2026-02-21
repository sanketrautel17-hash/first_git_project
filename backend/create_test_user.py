import requests

BASE_URL = "http://127.0.0.1:8000"


def create_user():
    email = "sanketrautel846@gmail.com"
    payload = {
        "first_name": "Sanket",
        "last_name": "Test",
        "email": email,
        "mobile_number": "1234567890",
        "password": "Password123",  # Satisfies Validations
        "address": {
            "street_address": "123 Test St",
            "city": "Test City",
            "state": "Test State",
            "postal_code": "12345",
            "country": "India",
        },
    }

    print(f"Creating user: {email}...")
    try:
        response = requests.post(f"{BASE_URL}/v1/users", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        if (
            response.status_code == 200 or response.status_code == 500
        ):  # 500 might mean "Already exists" based on my reading of controller which raises 500 for duplication? No, it handles it?
            # Controller:
            # if user: raise HTTPException(500, detail="User with this email already exist")
            # So 500 is likely "Already exists".
            print("User creation attempt finished.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    create_user()
