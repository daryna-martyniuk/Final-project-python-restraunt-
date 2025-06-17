from typing import Optional
from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict

class OrderItemBase(BaseModel):
    dish_id: int
    order_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = None

class OrderItemResponse(OrderItemBase):
    id: int
    price_at_order: float

    model_config = SettingsConfigDict(from_attributes=True)
