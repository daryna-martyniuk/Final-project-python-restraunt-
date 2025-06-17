from typing import Optional
from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class DishBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    category_id: int

class DishCreate(DishBase):
    pass

class DishUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    category_id: Optional[int] = None

class DishResponse(DishBase):
    id: int

    model_config = SettingsConfigDict(from_attributes=True)