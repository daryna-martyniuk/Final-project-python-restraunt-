from typing import List
from fastapi import HTTPException, status
from fastapi.params import Depends
from typing import Annotated

from app.crud.order_item import OrderItemRepoDep
from app.crud.dish import DishRepoDep
from app.crud.order import OrderRepoDep
from app.schemas.order_item import OrderItemCreate, OrderItemUpdate, OrderItemResponse


class OrderItemService:
    def __init__(self, order_item_repo: OrderItemRepoDep, dish_repo: DishRepoDep, order_repo: OrderRepoDep):
        self.order_item_repo = order_item_repo
        self.dish_repo = dish_repo
        self.order_repo = order_repo

    def get_all(self) -> List[OrderItemResponse]:
        items = self.order_item_repo.get_all()
        return [OrderItemResponse.model_validate(i) for i in items]

    def get_by_id(self, order_item_id: int) -> OrderItemResponse:
        item = self.order_item_repo.get_by_id(order_item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OrderItem not found")
        return OrderItemResponse.model_validate(item)

    def get_by_order_id(self, order_id: int) -> List[OrderItemResponse]:
        items = self.order_item_repo.get_by_order_id(order_id)
        if not items:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order items not found")
        return [OrderItemResponse.model_validate(i) for i in items]

    def create(self, order_item_create: OrderItemCreate) -> OrderItemResponse:
        if order_item_create.quantity < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity must be at least 1"
            )

        dish = self.dish_repo.get_by_id(order_item_create.dish_id)
        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dish not found"
            )

        order = self.order_repo.get_by_id(order_item_create.order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        if order.is_completed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot add items to completed order"
            )

        existing_items = self.order_item_repo.get_by_order_id(order_item_create.order_id)
        for item in existing_items:
            if item.dish_id == order_item_create.dish_id:
                updated_quantity = item.quantity + order_item_create.quantity
                updated_item = self.order_item_repo.update(
                    item.id,
                    OrderItemUpdate(quantity=updated_quantity))
                return OrderItemResponse.model_validate(updated_item)

        order_item_data = order_item_create.model_dump()
        order_item_data["price_at_order"] = dish.price
        created_item = self.order_item_repo.create(OrderItemCreate(**order_item_data))
        return OrderItemResponse.model_validate(created_item)

    def update(self, order_item_id: int, order_item_update: OrderItemUpdate) -> OrderItemResponse:
        order_item = self.order_item_repo.get_by_id(order_item_id)
        if not order_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OrderItem not found")

        if order_item_update.quantity is not None and order_item_update.quantity < 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity must be at least 1")

        order = self.order_repo.get_by_id(order_item.order_id)
        if order.is_completed:
            raise HTTPException(status_code=400, detail="Not allowed to update order items for completed order")

        update_data = order_item_update.model_dump(exclude_unset=True)

        updated_item = self.order_item_repo.update(order_item_id, order_item_update.__class__(**update_data))
        return OrderItemResponse.model_validate(updated_item)

    def delete(self, order_item_id: int) -> bool:
        order_item = self.order_item_repo.get_by_id(order_item_id)
        if not order_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OrderItem not found")
        order = self.order_repo.get_by_id(order_item.order_id)
        if order.is_completed:
            raise HTTPException(status_code=400, detail="Not allowed to delete order items for completed order")

        return self.order_item_repo.delete(order_item_id)


OrderItemCoreDep = Annotated[OrderItemService, Depends(OrderItemService)]