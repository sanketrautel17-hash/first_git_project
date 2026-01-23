from pydantic import BaseModel, Field


class PaymentRequest(BaseModel):
    order_id: int = Field(description="Id of the order")
    payment_type: str = Field(description="Type of the payment")
    amount: float = Field(description="Price of the order")
    total_amount: float = Field(description="Total amount of the order")
