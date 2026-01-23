from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    id: int = Field(description="Id of the user")
    name: str = Field(description="Name of the user")
    email: str = Field(description="Email of the user")
    mobile_number: str = Field(
        min_length=10, max_length=10, description="Mobile number of the user"
    )
    age: int = Field(description="Age of the user")
    gender: str = Field(description="Gender of the user")
