from datetime import date, time
from typing import List, Optional
from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict
from app.schemas.dish import DishResponse

class PromotionBase(BaseModel):
    description: str
    discount_percent: int
    valid_from: date
    valid_to: date
    start_time: Optional[time] = None
    end_time: Optional[time] = None

class PromotionCreate(PromotionBase):
    dish_ids: List[int]

class PromotionUpdate(BaseModel):
    description: Optional[str] = None
    discount_percent: Optional[int] = None
    valid_from: Optional[date] = None
    valid_to: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    dish_ids: Optional[List[int]] = None

class PromotionResponse(PromotionBase):
    id: int
    dishes: List[DishResponse]

    model_config = SettingsConfigDict(from_attributes=True)
