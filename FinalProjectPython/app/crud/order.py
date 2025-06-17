from datetime import datetime

from fastapi import Depends
from sqlalchemy import select, and_
from typing import Annotated

from sqlalchemy.orm import selectinload, joinedload

from app.db import SessionContext
from app.models.models import Order, OrderItem, Dish
from app.schemas.order import OrderCreate, OrderUpdate


class OrderRepo:
    def __init__(self, db: SessionContext):
        self.db = db

    def get_all(self) -> list[Order]:
        stmt = select(Order)
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_by_id(self, order_id: int) -> Order | None:
        stmt = select(Order).where(Order.id == order_id)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def get_active_orders(self) -> list[Order] :
        stmt = select(Order).where(Order.is_completed == False)
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_orders_by_period(self, start: datetime, end: datetime) -> list[Order]:
        stmt = (
            select(Order)
            .where(
                and_(
                    Order.created_at >= start,
                    Order.created_at <= end
                )
            )
            .options(joinedload(Order.items))
        )
        result = self.db.execute(stmt).unique()
        return result.unique().scalars().all()

    def create(self, data: OrderCreate) -> Order:
        order = Order(table_id=data.table_id, is_completed=False)
        self.db.add(order)
        self.db.flush()

        for item_data in data.items:
            dish_stmt = select(Dish).where(Dish.id == item_data.dish_id)
            dish_result = self.db.execute(dish_stmt)
            dish = dish_result.scalar_one()
            order_item = OrderItem(
                dish_id=item_data.dish_id,
                order_id=order.id,
                quantity=item_data.quantity,
                price_at_order=dish.price,
            )
            self.db.add(order_item)

        self.db.commit()
        self.db.refresh(order)
        return order

    def update(self, order_id: int, data: OrderUpdate) -> Order | None:
        order = self.get_by_id(order_id)
        if not order:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(order, key, value)
        self.db.commit()
        self.db.refresh(order)
        return order

    def complete_order(self, order_id: int) -> Order | None:
        order = self.get_by_id(order_id)
        if not order:
            return None
        order.is_completed = True
        self.db.commit()
        self.db.refresh(order)
        return order

    def delete(self, order_id: int) -> bool:
        order = self.get_by_id(order_id)
        if not order:
            return False
        self.db.delete(order)
        self.db.commit()
        return True


OrderRepoDep = Annotated[OrderRepo, Depends(OrderRepo)]
