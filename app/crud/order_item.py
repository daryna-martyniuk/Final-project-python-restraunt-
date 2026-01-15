from fastapi.params import Depends
from sqlalchemy import select
from typing import Annotated

from app.db import SessionContext
from app.models.models import OrderItem
from app.schemas.order_item import OrderItemCreate, OrderItemUpdate


class OrderItemRepo:
    def __init__(self, db: SessionContext):
        self.db = db

    def get_all(self) -> list[OrderItem]:
        stmt = select(OrderItem)
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_by_id(self, order_item_id: int) -> OrderItem | None:
        stmt = select(OrderItem).where(OrderItem.id == order_item_id)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def get_by_order_id(self, order_id: int) -> list[OrderItem]:
        stmt = select(OrderItem).where(OrderItem.order_id == order_id)
        result = self.db.execute(stmt)
        return result.scalars().all()

    def create(self, data: OrderItemCreate) -> OrderItem:
        order_item = OrderItem(**data.model_dump())
        self.db.add(order_item)
        self.db.commit()
        self.db.refresh(order_item)
        return order_item

    def update(self, order_item_id: int, data: OrderItemUpdate) -> OrderItem | None:
        order_item = self.get_by_id(order_item_id)
        if not order_item:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(order_item, key, value)
        self.db.commit()
        self.db.refresh(order_item)
        return order_item

    def delete(self, order_item_id: int) -> bool:
        order_item = self.get_by_id(order_item_id)
        if not order_item:
            return False
        self.db.delete(order_item)
        self.db.commit()
        return True

    def delete_order_items_by_order_id(self, order_item_id: int) -> bool:
        order_items = self.db.select(OrderItem).where(OrderItem.order_id == order_item_id)
        self.db.delete(order_items)
        self.db.commit()

OrderItemRepoDep = Annotated[OrderItemRepo, Depends(OrderItemRepo)]