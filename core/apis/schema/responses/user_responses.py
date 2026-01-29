from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from odmantic import ObjectId
from core.models.user_model import UserStatus


class AddressResponse(BaseModel):
    street_address: str = Field(description="Enter the address")
    city: str = Field(description="City name")
    state: str = Field(description="State or province")
    postal_code: str = Field(description="ZIP or postal code")
    country: str = Field(description="Country name")


class UserResponse(BaseModel):
    id: ObjectId = Field(description="Unique identifier of the user")
    first_name: str = Field(description="User's first name")
    last_name: str = Field(description="User's last name")
    email: EmailStr = Field(description="User's email address")
    mobile_number: str = Field(description="User's mobile number")
    address: Optional[AddressResponse] = Field(
        default=None, description="User's physical address"
    )
    status: UserStatus = Field(description="User account status")
    created_at: datetime = Field(description="Date and time when the user was created")
    updated_at: datetime = Field(
        description="Date and time when the user was last updated"
    )

    class Config:
        arbitrary_types_allowed = True
