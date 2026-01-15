from fastapi import APIRouter
from typing import List
from pydantic import PositiveInt

from app.core.order_item import OrderItemCoreDep
from app.schemas.order_item import OrderItemCreate, OrderItemUpdate, OrderItemResponse

router = APIRouter(
    prefix="/order-items",
    tags=["Order Items"]
)


@router.get("/", response_model=List[OrderItemResponse])
def get_all(service: OrderItemCoreDep):
    return service.get_all()


@router.get("/{order_item_id}", response_model=OrderItemResponse)
def get_by_id(order_item_id: PositiveInt, service: OrderItemCoreDep):
    return service.get_by_id(order_item_id)

@router.get("/get_by_order_id/{order_id}", response_model=List[OrderItemResponse])
def get_by_order_id(order_id: PositiveInt, service: OrderItemCoreDep):
    return service.get_by_order_id(order_id)

@router.post("/", response_model=OrderItemResponse)
def create(data: OrderItemCreate, service: OrderItemCoreDep):
    return service.create(data)


@router.put("/{order_item_id}", response_model=OrderItemResponse)
def update(order_item_id: PositiveInt, data: OrderItemUpdate, service: OrderItemCoreDep):
    return service.update(order_item_id, data)


@router.delete("/{order_item_id}")
def delete(order_item_id: PositiveInt, service: OrderItemCoreDep):
    return service.delete(order_item_id)
