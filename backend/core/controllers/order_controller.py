from core.cruds.order_crud import OrderCRUD
from commons.auth import signJWT
from core.apis.schemas.requests.order_request import OrderRequest
from core.apis.schemas.responses.order_response import OrderResponse
from fastapi import HTTPException
from commons.logger import logger
from odmantic import ObjectId

logging = logger(__name__)


class OrderController:
    def __init__(self):
        self.OrderCRUD = OrderCRUD()

    async def create_order(self, order_request: dict):
        try:
            logging.info("Executing OrderController.create_order")
            if order_request.get("order_id"):
                order = await self.OrderCRUD.get_order_by_order_id(
                    order_request.get("order_id")
                )
                if order:
                    logging.info("Order id already exist")
                    raise HTTPException(
                        status_code=409, detail="Order id already exist"
                    )

            # Convert user_id string to ObjectId
            if "created_by" in order_request and isinstance(
                order_request["created_by"], str
            ):
                order_request["created_by"] = ObjectId(order_request["created_by"])

            saved_order = await self.OrderCRUD.create_order(order_request)
            access_token = signJWT(
                id=str(saved_order.id),
                expiry_duration=3600,
                status=saved_order.order_status.value,
            )
            result = saved_order.model_dump()
            result["id"] = str(saved_order.id)

            return {"Order": result, "access_token": access_token}

        except HTTPException as error:
            logging.error(f"Error in OrderController.create_order {str(error)}")
            raise error

    async def delete_order(self, order_id: str, user_id: str):
        try:
            logging.info("Executing OrderController.delete_order")
            order = await self.OrderCRUD.get_order_by_order_id(order_id)
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")

            if str(order.created_by) != user_id:
                raise HTTPException(
                    status_code=403,
                    detail="You are not authorized to delete this order",
                )

            await self.OrderCRUD.delete_order(order_id)
            return {"message": "Order deleted successfully"}
        except HTTPException as error:
            logging.error(f"Error in OrderController.delete_order {str(error)}")
            raise error

    async def update_order(self, order_id: str, request: dict, user_id: str):
        try:
            logging.info("Executing OrderController.update_order")
            order = await self.OrderCRUD.get_order_by_order_id(order_id)
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")

            if str(order.created_by) != user_id:
                raise HTTPException(
                    status_code=403,
                    detail="You are not authorized to update this order",
                )

            updated_order = await self.OrderCRUD.update_order(order_id, request)
            return updated_order
        except HTTPException as error:
            logging.error(f"Error in OrderController.update_order {str(error)}")
            raise error

    async def get_user_orders(self, user_id: str):
        try:
            logging.info("Executing OrderController.get_user_orders")
            orders = await self.OrderCRUD.get_orders_by_user(user_id)
            # Convert ObjectId to string for response
            result = []
            for order in orders:
                logging.info(f"DEBUG ITEMS: {order.order_items}")
                order_dict = order.model_dump()
                order_dict["id"] = str(order.id)
                order_dict["created_by"] = str(order.created_by)
                result.append(order_dict)
            return result
        except HTTPException as error:
            logging.error(f"Error in OrderController.get_user_orders {str(error)}")
            raise error
