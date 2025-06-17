from pydantic import BaseModel
from typing import Optional

from pydantic_settings import SettingsConfigDict


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int

    model_config = SettingsConfigDict(from_attributes=True)