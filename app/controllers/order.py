from datetime import date

from fastapi import APIRouter, Query
from typing import List
from pydantic import PositiveInt

from app.core.order import OrderCoreDep
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.get("/by-period", response_model=List[OrderResponse])
def get_orders_by_period(
    service: OrderCoreDep,
    start_date: date = Query(
        description="Start date YYYY-MM-DD",
        example="2025-06-01"
    ),
    end_date: date = Query(
        description="End date YYYY-MM-DD",
        example="2025-06-08"
    )):
    return service.get_orders_by_period(start_date, end_date)
@router.get("/", response_model=List[OrderResponse])
def get_all(service: OrderCoreDep):
    return service.get_all()


@router.get("/{order_id}", response_model=OrderResponse)
def get_by_id(order_id: PositiveInt, service: OrderCoreDep):
    return service.get_by_id(order_id)

@router.get("/active/", response_model=List[OrderResponse])
def get_active_orders(service: OrderCoreDep):
    return service.get_active_orders()


@router.post("/", response_model=OrderResponse)
def create(data: OrderCreate, service: OrderCoreDep):
    return service.create(data)


@router.put("/{order_id}", response_model=OrderResponse)
def update(order_id: PositiveInt, data: OrderUpdate, service: OrderCoreDep):
    return service.update(order_id, data)

@router.put("/{order_id}/complete", response_model=OrderResponse)
def complete(order_id: PositiveInt, service: OrderCoreDep):
    return service.complete_order(order_id)

@router.delete("/{order_id}")
def delete(order_id: PositiveInt, service: OrderCoreDep):
    return service.delete(order_id)


@router.get("/{order_id}/total")
def calculate_total(order_id: PositiveInt, service: OrderCoreDep):
    return {"total": service.calculate_total(order_id)}
