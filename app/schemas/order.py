from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict
from app.schemas.order_item import OrderItemCreate, OrderItemResponse
from app.schemas.cafe_table import CafeTableResponse

class OrderBase(BaseModel):
    table_id: int

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    table_id: Optional[int] = None
    is_completed: Optional[bool] = None

class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    is_completed: Optional[bool]
    items: List[OrderItemResponse]
    table: Optional[CafeTableResponse]

    model_config = SettingsConfigDict(from_attributes=True)
