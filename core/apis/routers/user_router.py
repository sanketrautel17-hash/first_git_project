from fastapi import HTTPException
from fastapi import APIRouter
from core.apis.schema.responses.user_responses import UserResponse
from core.apis.schema.requests.user_requests import UserRequest, UserUpdateRequest

user_router = APIRouter()

user_list = []


@user_router.post("/v1/create-user")
def create_user(request: UserRequest):
    try:
        # Check for duplicate email
        for user in user_list:
            if user["email"] == request.email:
                raise HTTPException(status_code=409, detail="User already exists")

        # Generate new ID
        if user_list:
            new_id = user_list[-1]["id"] + 1
        else:
            new_id = 1

        # Create user data and add to list
        user_data = request.model_dump()
        user_data["id"] = new_id
        user_list.append(user_data)

        return {"message": "User created successfully"}

    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@user_router.get("/v1/get-user")
def get_user():
    try:
        return user_list
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@user_router.get("/v1/get-user/{user_id}")
def get_user_by_id(user_id: int):
    try:
        for user in user_list:
            if user["id"] == user_id:
                return UserResponse(**user)
        raise HTTPException(status_code=404, detail="User not found")

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@user_router.patch("/v1/update-user/{user_id}")
def update_user(user_id: int, request: UserUpdateRequest):
    try:
        for user in user_list:
            if user["id"] == user_id:
                update_data = request.model_dump(exclude_unset=True)
                user.update(update_data)
                return UserResponse(**user)

        raise HTTPException(status_code=404, detail="User not found")

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@user_router.delete("/v1/delete-user/{user_id}")
def delete_user(user_id: int):
    try:
        for user in user_list:
            if user["id"] == user_id:
                user_list.pop(user)
                return {"message": "User deleted successfully"}
        raise HTTPException(status_code=404, detail="User not found")

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
