from pydantic import BaseModel, Field
from typing import Optional


class UserRequest(BaseModel):
    name: str = Field(description="Name of the user")
    email: str = Field(description="Email of the user")
    password: str = Field(
        min_length=5, max_length=10, description="Password of the user"
    )
    mobile_number: str = Field(
        min_length=10, max_length=10, description="Mobile number of the user"
    )
    age: int = Field(description="Age of the user")
    gender: str = Field(description="Gender of the user")


class UserUpdateRequest(BaseModel):
    """Schema for partial user updates - all fields are optional"""

    name: Optional[str] = Field(default=None, description="Name of the user")
    email: Optional[str] = Field(default=None, description="Email of the user")
    password: Optional[str] = Field(
        default=None, min_length=5, max_length=10, description="Password of the user"
    )
    mobile_number: Optional[str] = Field(
        default=None,
        min_length=10,
        max_length=10,
        description="Mobile number of the user",
    )
    age: Optional[int] = Field(default=None, description="Age of the user")
    gender: Optional[str] = Field(default=None, description="Gender of the user")
