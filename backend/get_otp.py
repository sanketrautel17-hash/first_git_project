import asyncio
from core.database.database import get_engine, connect_to_mongo
from core.models.user_model import User


async def get_otp():
    await connect_to_mongo()
    email = "sanketrautel846@gmail.com"
    engine = get_engine()
    user = await engine.find_one(User, User.email == email)
    if user:
        print(f"OTP for {email}: {user.otp_code}")
    else:
        print("User not found")


if __name__ == "__main__":
    asyncio.run(get_otp())
