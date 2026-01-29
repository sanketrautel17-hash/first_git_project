from core.models.user_model import UserModel
from commons.loggers import logger
from core.database.database import get_engine
from fastapi import HTTPException

logging = logger(__name__)


class UserCRUD:
    def __init__(self):
        self.engine = get_engine()

    async def create_user(self, user: dict):
        try:
            logging.info("Executing UserCRUD.create_user")
            saved_user = await self.engine.save(UserModel(**user))
            logging.info(f"User created successfully:{saved_user.id}")
            return saved_user

        except Exception as error:
            logging.error(f"Error in UserCRUD.create_user: {str(error)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    async def get_by_email(self, email: str):
        try:
            logging.info("Executing UserCRUD.get_by_email")
            user = await self.engine.find_one(UserModel, UserModel.email == email)
            if user:
                logging.info(f"User found successfully {email}")
            else:
                logging.info(f"User not found with this email {email}")
                return None
            return user
        except Exception as error:
            logging.error(f"Error in UserCRUD.get_by_email: {str(error)}")
            raise HTTPException(status_code=500, detail="Internal server error")
