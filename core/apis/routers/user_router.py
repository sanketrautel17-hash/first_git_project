from fastapi import HTTPException
from fastapi import APIRouter
from core.apis.schema.responses.user_responses import UserResponse
from core.apis.schema.requests.user_requests import UserCreateRequest, UserUpdateRequest
from commons.loggers import logger
from core.controllers.user_controller import UserController


user_router = APIRouter()

logging = logger(__name__)


@user_router.post("/v1/users")
async def create_user(user_request: UserCreateRequest):
    try:
        logging.info("Executing UserRouter.create_user")
        request = user_request.model_dump()
        result = await UserController().create_user(request)
        return result

    except HTTPException:
        raise
    except Exception as error:
        logging.error(f"Error in UserRouter.create_user: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")
