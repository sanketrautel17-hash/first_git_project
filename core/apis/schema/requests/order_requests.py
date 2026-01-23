from pydantic import BaseModel, Field


class OrderRequest(BaseModel):
    user_id: int = Field(description="Id of the user")
    product_name: str = Field(description="Name of the product")
    product_price: float = Field(description="Price of the product")
    quantity: int = Field(description="Quantity of the product")
    total_amount: float = Field(description="Total amount of the order")
