from odmantic import ObjectId
from core.models.order_model import Order
from commons.logger import logger
from core.database.database import get_engine
from fastapi import HTTPException

logging = logger(__name__)


class OrderCRUD:
    def __init__(self):
        self.Order = Order
        self.engine = get_engine()

    async def create_order(self, order: dict):
        try:
            logging.info("Executing OrderCRUD.create_order")
            saved_order = await self.engine.save(Order(**order))
            logging.info(f"Order created with id: {saved_order.id}")
            return saved_order
        except HTTPException as error:
            logging.error(f"Error in OrderCRUD.create {str(error)}")
            raise error

    async def get_order_by_order_id(self, order_id: int):
        try:
            logging.info("Executing OrderCRUD.get_order_by_order_id")
            order_id = ObjectId(order_id)
            order = await self.engine.find_one(Order, Order.id == order_id)
            if order:
                logging.info(f"Order found with id: {order_id}")
            else:
                logging.info(f"Order not found with id: {order_id}")
            return order

        except HTTPException as error:
            logging.error(f"Error in OrderCRUD.get_order_by_order_id {str(error)}")
            raise error

    async def get_orders_by_user(self, user_id: str):
        try:
            logging.info("Executing OrderCRUD.get_orders_by_user")
            user_id = ObjectId(user_id)
            # Use 'created_by' field as defined in Order model
            orders = await self.engine.find(Order, Order.created_by == user_id)
            if orders:
                logging.info(f"Orders found for user_id: {user_id}")
            else:
                logging.info(f"No orders found for user_id: {user_id}")
            return orders
        except HTTPException as error:
            logging.error(f"Error in OrderCRUD.get_orders_by_user {str(error)}")
            raise error

    async def delete_order(self, order_id: str):
        try:
            logging.info("Executing OrderCRUD.delete_order")
            order_id = ObjectId(order_id)
            order = await self.engine.find_one(Order, Order.id == order_id)
            if order:
                await self.engine.delete(order)
                logging.info(f"Order deleted with id: {order_id}")
                return True
            return False
        except HTTPException as error:
            logging.error(f"Error in OrderCRUD.delete_order {str(error)}")
            raise error

    async def update_order(self, order_id: str, details: dict):
        try:
            logging.info("Executing OrderCRUD.update_order")
            order_id = ObjectId(order_id)
            order = await self.engine.find_one(Order, Order.id == order_id)
            if order:
                for key, value in details.items():
                    if hasattr(order, key):
                        setattr(order, key, value)
                await self.engine.save(order)
                logging.info(f"Order updated with id: {order_id}")
                return order
            return None
        except HTTPException as error:
            logging.error(f"Error in OrderCRUD.update_order {str(error)}")
            raise error
