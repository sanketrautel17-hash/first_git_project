from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from core.models.order_model import OrderStatus


class OrderResponseAddress(BaseModel):

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


class OrderResponse(BaseModel):
    order_id: str = Field(..., description="Order ID")
    created_by: str = Field(..., description="User ID who created the order")
    order_items: List[dict] = Field(..., description="List of items in the order")
    order_number: str = Field(..., description="Order number")
    order_price: float = Field(..., description="Price of the order")
    order_quantity: int = Field(..., description="Quantity of items")
    total_amount: float = Field(..., description="Total amount for the order")
    address: Optional[OrderResponseAddress] = Field(
        None, description="Shipping address"
    )
    order_status: OrderStatus = Field(..., description="Status of the order")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = {"from_attributes": True}
