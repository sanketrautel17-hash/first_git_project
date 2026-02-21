import asyncio
import httpx
import sys
import os

# Add the parent directory to sys.path to resolve imports if necessary
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://127.0.0.1:8000"


async def test_order_flow():
    async with httpx.AsyncClient(timeout=30.0) as client:
        print("\n--- 1. Creating User & Login ---")
        # 1. Create unique user
        import time

        rand_id = int(time.time())
        email = f"testorder{rand_id}@example.com"
        password = "Password123!"

        user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": email,
            "password": password,
            "mobile_number": "1234567890",
        }

        # Register
        resp = await client.post(f"{BASE_URL}/v1/users", json=user_data)
        if resp.status_code != 200:
            print(f"User creation failed: {resp.text}")
            return
        print(f"User created: {resp.json().get('email')}")

        # Login
        login_data = {"email": email, "password": password}
        resp = await client.post(f"{BASE_URL}/v1/login", json=login_data)
        if resp.status_code != 200:
            print(f"Login failed: {resp.text}")
            return

        token = resp.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        print("Login successful, token received.")

        print("\n--- 2. Create Order ---")
        order_data = {
            "order_number": f"{rand_id}",
            "order_price": 100.50,
            "order_quantity": 2,
            "total_amount": 201.00,
            "order_items": [{"item_id": "1", "name": "Test Widget", "price": 100.50}],
            "address": {
                "street_address": "123 Test St",
                "city": "Test City",
                "state": "Test State",
                "postal_code": "12345",
                "country": "India",
            },
        }

        resp = await client.post(
            f"{BASE_URL}/v1/orders", json=order_data, headers=headers
        )
        if resp.status_code != 200:
            print(f"Create Order Failed: {resp.text}")
            return

        order_response = resp.json().get(
            "Order"
        )  # Assuming structure { "Order": {...}, "access_token": ...}
        if not order_response:
            # Fallback if structure is different
            order_response = resp.json()

        order_id = order_response.get("id")
        created_by = order_response.get("created_by")
        print(f"Order Created! ID: {order_id}, User: {created_by}")
        print(f"Items: {order_response.get('order_items')}")

        print("\n--- 3. Update Order ---")
        update_data = {"order_quantity": 5, "total_amount": 502.50}

        resp = await client.patch(
            f"{BASE_URL}/v1/orders/{order_id}", json=update_data, headers=headers
        )
        if resp.status_code == 200:
            updated_order = resp.json()
            print(f"Order Updated! New Quantity: {updated_order.get('order_quantity')}")
            if updated_order.get("order_quantity") == 5:
                print("SUCCESS: Update Verified.")
            else:
                print("FAILURE: Update value mismatch.")
        else:
            print(f"Update Failed: {resp.text}")

        print("\n--- 4. Delete Order ---")
        resp = await client.delete(f"{BASE_URL}/v1/orders/{order_id}", headers=headers)
        if resp.status_code == 200:
            print("Order Deleted Successfully.")
        else:
            print(f"Delete Failed: {resp.text}")

        print("\n--- 5. Verify Deletion ---")
        # Try to delete again, should fail or return 404/400
        resp = await client.delete(f"{BASE_URL}/v1/orders/{order_id}", headers=headers)
        if resp.status_code == 404:
            print("SUCCESS: Order correctly not found after deletion.")
        else:
            print(f"Double Delete Status: {resp.status_code} (Expected 404)")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(test_order_flow())
