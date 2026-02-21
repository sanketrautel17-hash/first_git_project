from typing import List, Optional
from pydantic import BaseModel, Field


class OrderRequestAddress(BaseModel):

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


class OrderRequest(BaseModel):
    order_items: List[dict] = Field(..., description="List of items in the order")
    order_number: str = Field(
        ..., min_length=2, max_length=50, description="Order number"
    )
    order_price: float = Field(..., description="Price of the order")
    order_quantity: int = Field(..., description="Quantity of items")
    total_amount: float = Field(..., description="Total amount for the order")
    address: Optional[OrderRequestAddress] = Field(
        default=None, description="Shipping address"
    )
