from odmantic import ObjectId
from enum import Enum
from typing import Optional
from datetime import datetime

from odmantic import Field, Model
from pydantic import BaseModel, field_validator


class UserOrderAddress(BaseModel):

    street_address: str = Field(
        ...,
        min_length=5,
        max_length=200,
        description="Street address with house/building number",
    )
    city: str = Field(..., min_length=2, max_length=100, description="City name")
    state: str = Field(
        ..., min_length=2, max_length=100, description="State or province"
    )
    postal_code: str = Field(
        ..., min_length=5, max_length=10, description="ZIP or postal code"
    )
    country: str = Field(
        default="India", min_length=2, max_length=100, description="Country name"
    )


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Order(Model):
    created_by: ObjectId = Field(..., description="User ID")
    order_items: list = Field(..., description="Order items")
    order_number: str = Field(
        ..., min_length=2, max_length=50, description="Order number"
    )
    order_price: float = Field(..., description="Order price")
    order_quantity: int = Field(..., description="Order quantity")
    total_amount: float = Field(..., description="Total amount")
    address: Optional[UserOrderAddress] = Field(
        default=None, description="User's physical address"
    )
    order_status: OrderStatus = Field(
        default=OrderStatus.PENDING, description="Current account status"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Account creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="Last update timestamp"
    )

    @field_validator("order_number")
    @classmethod
    def validate_order_number(cls, value: str) -> str:
        """Validate that order number contains only digits."""
        cleaned = value.replace("+", "").replace("-", "").replace(" ", "")
        if not cleaned.isdigit():
            raise ValueError("Order number must contain only digits")
        return value

    model_config = {"collection": "orders", "extra": "ignore"}
