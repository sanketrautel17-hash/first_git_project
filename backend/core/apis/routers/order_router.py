from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from commons.auth import decodeJWT
from core.controllers.order_controller import OrderController
from core.apis.schemas.requests.order_request import OrderRequest
from commons.logger import logger

logging = logger(__name__)
order_router = APIRouter()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="v1/login")


@order_router.post("/v1/orders")
async def create_order(
    order_request: OrderRequest, token: str = Depends(oauth2_schema)
):
    try:
        logging.info("Calling /v1/orders endpoint")
        user_details = decodeJWT(token)
        if not user_details:
            raise HTTPException(status_code=401, detail="Invalid request")

        request = order_request.model_dump()
        request["created_by"] = user_details.get("id")
        result = await OrderController().create_order(request)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error creating order: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@order_router.delete("/v1/orders/{order_id}")
async def delete_order(order_id: str, token: str = Depends(oauth2_schema)):
    try:
        logging.info(f"Calling DELETE /v1/orders/{order_id}")
        user_details = decodeJWT(token)
        if not user_details:
            raise HTTPException(status_code=401, detail="Invalid request")

        result = await OrderController().delete_order(
            order_id=order_id, user_id=user_details.get("id")
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error deleting order: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@order_router.patch("/v1/orders/{order_id}")
async def update_order(
    order_id: str, order_request: OrderRequest, token: str = Depends(oauth2_schema)
):
    try:
        logging.info(f"Calling PATCH /v1/orders/{order_id}")
        user_details = decodeJWT(token)
        if not user_details:
            raise HTTPException(status_code=401, detail="Invalid request")

        request = order_request.model_dump(exclude_unset=True)
        result = await OrderController().update_order(
            order_id=order_id, request=request, user_id=user_details.get("id")
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating order: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@order_router.get("/v1/orders")
async def get_orders(token: str = Depends(oauth2_schema)):
    try:
        logging.info("Calling GET /v1/orders")
        user_details = decodeJWT(token)
        if not user_details:
            raise HTTPException(status_code=401, detail="Invalid request")

        result = await OrderController().get_user_orders(user_id=user_details.get("id"))
        return {"orders": result}
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error fetching orders: {e}")
        raise HTTPException(status_code=500, detail=str(e))
