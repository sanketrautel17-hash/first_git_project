from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional


class AddressRequest(BaseModel):
    street_address: str = Field(
        ..., min_length=5, max_length=200, description="Enter the address"
    )
    city: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="City name",
    )
    state: str = Field(
        ..., min_length=2, max_length=100, description="State or province"
    )
    postal_code: str = Field(
        ..., min_length=5, max_length=10, description="ZIP or postal code"
    )
    country: str = Field(
        default="India", min_length=2, max_length=100, description="Country name"
    )


class UserCreateRequest(BaseModel):
    first_name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="User's first name",
    )
    last_name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="User's last name",
    )
    email: EmailStr = Field(
        ...,
        description="User's email address (must be unique)",
    )
    mobile_number: str = Field(
        ...,
        min_length=10,
        max_length=15,
        description="User's mobile number with country code",
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="User's password (min 8 characters)",
    )
    address: Optional[AddressRequest] = Field(
        default=None,
        description="User's physical address (optional)",
    )

    @field_validator("mobile_number")
    @classmethod
    def validate_mobile_number(cls, value: str) -> str:
        """Validate that mobile number contains only digits (with optional + prefix)."""
        cleaned = value.replace("+", "").replace("-", "").replace(" ", "")
        if not cleaned.isdigit():
            raise ValueError("Mobile number must contain only digits")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        """Validate password strength."""
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")
        return value


class UserUpdateRequest(BaseModel):
    """Schema for partial user updates - all fields are optional"""

    first_name: Optional[str] = Field(default=None, description="User's first name")
    last_name: Optional[str] = Field(default=None, description="User's last name")
    email: Optional[EmailStr] = Field(default=None, description="User's email address")
    mobile_number: Optional[str] = Field(
        default=None, description="User's mobile number"
    )
    password: Optional[str] = Field(default=None, description="User's password")
    address: Optional[AddressRequest] = Field(
        default=None, description="User's physical address"
    )
