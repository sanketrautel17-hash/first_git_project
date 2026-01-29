from core.cruds.user_crud import UserCRUD
from fastapi import HTTPException
from commons.auth import signJWT
from commons.auth import encrypt_password
from commons.loggers import logger

logging = logger(__name__)


class UserController:
    def __init__(self):
        self.UserCRUD = UserCRUD()

    async def create_user(self, user_request: dict):
        try:
            logging.info("Calling v1/users endpoint")
            user = await self.UserCRUD.get_by_email(user_request.get("email", ""))
            if user:
                logging.warning("User with this email already exist")
                raise HTTPException(
                    status_code=409, detail="User with this email already exist"
                )
            user_request["hashed_password"] = encrypt_password(
                password=user_request.get("password", "")
            )
            user_request["status"] = "ACTIVE"
            user_request.pop("password", None)
            saved_user = await self.UserCRUD.create_user(user_request)
            access_token = signJWT(
                id=str(saved_user.id), expiry_duration=3600, user_status="ACTIVE"
            )
            result = saved_user.model_dump()
            result["id"] = str(saved_user.id)
            return {"user": result, "access_token": access_token}

        except HTTPException:
            raise
        except Exception as error:
            logging.error(f"Error in UserController.create_user: {str(error)}")
            raise HTTPException(status_code=500, detail="Internal server error")
