import asyncio
from datetime import datetime
from core.cruds.user_crud import UserCRUD
from core.database.database import connect_to_mongo, close_mongo_connection
from core.apis.schemas.requests.user_request import UserUpdateRequest
import logging

# Configure logging to see output
logging.basicConfig(level=logging.INFO)


async def test_cruds():
    print("--- Starting CRUD Operations Test ---")

    # 1. Connect to DB
    await connect_to_mongo()
    crud = UserCRUD()

    # Test Data
    test_email = f"crud_test_{int(datetime.utcnow().timestamp())}@example.com"
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": test_email,
        "mobile_number": "1234567890",
        "hashed_password": "hashed_secret_password",
        "status": "ACTIVE",
    }

    # 2. Test CREATE
    print(f"\n[1] Testing CREATE User ({test_email})...")
    try:
        created_user = await crud.create(user_data)
        print(f"✅ Success: User created with ID: {created_user.id}")
    except Exception as e:
        print(f"❌ Failed: {e}")
        return

    user_id = str(created_user.id)

    # 3. Test READ (Get by Email)
    print(f"\n[2] Testing GET BY EMAIL ({test_email})...")
    try:
        found_by_email = await crud.get_by_email(test_email)
        if found_by_email and found_by_email.id == created_user.id:
            print(f"✅ Success: User found by email.")
        else:
            print(f"❌ Failed: User not found or ID mismatch.")
    except Exception as e:
        print(f"❌ Failed: {e}")

    # 4. Test READ (Get by ID)
    print(f"\n[3] Testing GET BY ID ({user_id})...")
    try:
        found_by_id = await crud.get_by_id(user_id)
        if found_by_id and found_by_id.email == test_email:
            print(f"✅ Success: User found by ID.")
        else:
            print(f"❌ Failed: User not found or Email mismatch.")
    except Exception as e:
        print(f"❌ Failed: {e}")

    # 5. Test UPDATE
    print(f"\n[4] Testing UPDATE...")
    update_payload = {"first_name": "UpdatedName", "last_name": "UpdatedLast"}
    try:
        # We need to simulate the request object or pass dict if handled
        # The update method expects update_data which is converted to UserUpdateRequest
        # UserUpdateRequest fields are optional

        updated_user = await crud.update(user_id, update_payload)

        if updated_user and updated_user.first_name == "UpdatedName":
            print(f"✅ Success: User updated. New Name: {updated_user.first_name}")
        else:
            print(f"❌ Failed: Update returned None or name didn't change.")

    except Exception as e:
        print(f"❌ Failed: {e}")

    # 6. Verify Update with Read
    print(f"\n[5] Verifying Update with GET BY ID...")
    try:
        ver_user = await crud.get_by_id(user_id)
        if ver_user.first_name == "UpdatedName":
            print(f"✅ Success: Verified update persistence.")
        else:
            print(f"❌ Failed: Persistence check failed.")
    except Exception as e:
        print(f"❌ Failed: {e}")

    # Clean up (Manual Delete since no Delete CRUD)
    # create a delete functionality if needed

    await close_mongo_connection()
    print("\n--- CRUD Operations Test Completed ---")


if __name__ == "__main__":
    asyncio.run(test_cruds())
