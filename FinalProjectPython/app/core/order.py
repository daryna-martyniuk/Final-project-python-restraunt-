from typing import List
from fastapi import HTTPException, status
from datetime import datetime, date, time

from fastapi.params import Depends
from typing import Annotated

from app.crud.order import OrderRepoDep
from app.crud.order_item import OrderItemRepoDep
from app.crud.dish import DishRepoDep
from app.crud.promotion import PromotionRepoDep
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from app.schemas.order_item import OrderItemResponse
from app.crud.cafe_table import CafeTableRepoDep


class OrderService:
    def __init__(
        self,
        order_repo: OrderRepoDep,
        order_item_repo: OrderItemRepoDep,
        dish_repo: DishRepoDep,
        promotion_repo: PromotionRepoDep,
        table_repo: CafeTableRepoDep,
    ):
        self.order_repo = order_repo
        self.order_item_repo = order_item_repo
        self.dish_repo = dish_repo
        self.promotion_repo = promotion_repo
        self.table_repo = table_repo

    def get_all(self) -> List[OrderResponse]:
        orders = self.order_repo.get_all()
        return [OrderResponse.model_validate(o) for o in orders]

    def get_by_id(self, order_id: int) -> OrderResponse:
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        return OrderResponse.model_validate(order)

    def get_active_orders(self) -> List[OrderResponse]:
        orders = self.order_repo.get_active_orders()
        if not orders:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active orders")
        return [OrderResponse.model_validate(o) for o in orders]

    def get_orders_by_period(self, start_date: date, end_date: date) -> List[OrderResponse]:
        start_datetime = datetime.combine(start_date, time.min)
        end_datetime = datetime.combine(end_date, time.max)
        if start_datetime > end_datetime:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Start date must be before end date")

        orders = self.order_repo.get_orders_by_period(
            start=start_datetime,
            end=end_datetime
        )
        if not orders:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orders not found")
        return [OrderResponse.model_validate(o) for o in orders]

    def create(self, order_create: OrderCreate) -> OrderResponse:
        table = self.table_repo.get_by_id(order_create.table_id)
        if not table:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Table id {order_create.table_id} not found"
            )
        if self.table_repo.is_table_occupied(table.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Table {table.id} already has an active order."
            )
        for item in order_create.items:
            dish = self.dish_repo.get_by_id(item.dish_id)
            if not dish:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Dish id {item.dish_id} not found")
            if item.quantity <= 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity must be positive")

        order = self.order_repo.create(order_create)

        return OrderResponse.model_validate(order)

    def update(self, order_id: int, order_update: OrderUpdate) -> OrderResponse:
        order = self.order_repo.update(order_id, order_update)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        table = self.table_repo.get_by_id(order_update.table_id)
        if not table:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Table id {order_update.table_id} not found"
            )
        if self.table_repo.is_table_occupied(table.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Table {table.id} already has an active order."
            )
        return OrderResponse.model_validate(order)

    def complete_order(self, order_id: int) -> OrderResponse:
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        if order.is_completed:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order already completed")
        competed_order = self.order_repo.complete_order(order_id)
        return OrderResponse.model_validate(competed_order)

    def delete(self, order_id: int) -> bool:
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        if not order.is_completed:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order is not completed")
        self.order_repo.delete(order_id)
        return True

    def calculate_total(self, order_id: int) -> float:
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        now = datetime.utcnow().date()

        order_items = self.order_item_repo.get_by_order_id(order_id)
        if not order_items:
            return 0.0

        dish_totals = {item.dish_id: (item.price_at_order, item.quantity) for item in order_items}

        active_promotions = self.promotion_repo.get_active_promotion()

        total_without_discount = sum(price * quantity for price, quantity in dish_totals.values())

        total_discount = 0.0
        for promo in active_promotions:
            for dish in promo.dishes:
                dish_id = dish.id
                if dish_id in dish_totals:
                    price, quantity = dish_totals[dish_id]
                    discount_amount = price * quantity * (promo.discount_percent / 100)
                    total_discount += discount_amount

        total = total_without_discount - total_discount
        return max(total, 0.0)


OrderCoreDep = Annotated[OrderService, Depends(OrderService)]
