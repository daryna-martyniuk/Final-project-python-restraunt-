from pydantic import BaseModel
from typing import Optional
from pydantic_settings import SettingsConfigDict

class CafeTableBase(BaseModel):
    number: int
    location: Optional[str] = None

class CafeTableCreate(CafeTableBase):
    pass

class CafeTableUpdate(BaseModel):
    number: Optional[int] = None
    location: Optional[str] = None

class CafeTableResponse(CafeTableBase):
    id: int

    model_config = SettingsConfigDict(from_attributes=True)
