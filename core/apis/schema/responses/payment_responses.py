from pydantic import BaseModel, Field


class PaymentResponse(BaseModel):
    payment_id: int = Field(description="Id of the payment")
    order_id: int = Field(description="Id of the order")
    payment_type: str = Field(description="Type of the payment")
    amount: float = Field(description="Price of the order")
    total_amount: float = Field(description="Total amount of the order")
