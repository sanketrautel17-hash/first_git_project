import requests
import json
import time

BASE_URL = "http://127.0.0.1:8001"


def test_forget_password_flow():
    print("--- Testing Forget Password Flow ---")

    # 1. Ask for Email
    email = input(
        "Enter the email address to test with (must be a registered user): "
    ).strip()
    if not email:
        print("Email is required.")
        return

    # Debug: Check if Router is mounted
    print("Checking /v1/test_logs...")
    try:
        r = requests.get(f"{BASE_URL}/v1/test_logs")
        print(f"Test Logs Status: {r.status_code}")
    except:
        print("Could not hit /v1/test_logs")

    print("Checking /v1/users (GET)...")
    try:
        r = requests.get(f"{BASE_URL}/v1/users")
        print(
            f"Users GET Status: {r.status_code}"
        )  # Expect 405 or 200? It is POST only, so 405.
    except:
        print("Could not hit /v1/users")

    # 2. Trigger Forget Password

    # 2. Trigger Forget Password
    print(f"\n[1] Requesting OTP for {email}...")
    try:
        response = requests.post(
            f"{BASE_URL}/v1/forget-password", json={"email": email}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code != 200:
            print("Failed to send OTP. Exiting.")
            return
    except Exception as e:
        print(f"Error connecting to server: {e}")
        return

    # 3. Ask for OTP
    print("\nCheck your email for the OTP.")
    otp = input("Enter the 4-digit OTP you received: ").strip()

    # 4. Ask for New Password
    new_password = "NewPassword123"
    print(f"\nSetting new password to: {new_password}")

    # 5. Reset Password
    print("\n[2] Resetting password...")
    payload = {
        "email": email,
        "otp": otp,
        "new_password": new_password,
        "confirm_password": new_password,
    }

    try:
        response = requests.post(f"{BASE_URL}/v1/reset-password-otp", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            print("\nSUCCESS: Password reset successfully!")

            # 6. Verify Login
            print("\n[3] Verifying Login with new password...")
            login_payload = {"email": email, "password": new_password}
            login_resp = requests.post(f"{BASE_URL}/v1/login", json=login_payload)
            print(f"Login Status: {login_resp.status_code}")
            if login_resp.status_code == 200:
                print("Login Successful!")
            else:
                print(f"Login Failed: {login_resp.text}")
        else:
            print("Failed to reset password.")

    except Exception as e:
        print(f"Error connecting to server: {e}")


if __name__ == "__main__":
    test_forget_password_flow()
