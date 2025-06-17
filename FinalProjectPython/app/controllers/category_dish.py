from fastapi import APIRouter
from typing import List
from pydantic import PositiveInt

from app.core.category_dish import CategoryCoreDep  # твоя залежність сервісу категорій
from app.schemas.category_dish import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.get("/", response_model=List[CategoryResponse])
def get_all(service: CategoryCoreDep):
    return service.get_all()


@router.get("/{category_id}", response_model=CategoryResponse)
def get_by_id(category_id: PositiveInt, service: CategoryCoreDep):
    return service.get_by_id(category_id)

@router.get("/name/{category_name}", response_model=CategoryResponse)
def get_by_name(category_name: str, service: CategoryCoreDep):
    return service.get_by_name(category_name)

@router.post("/", response_model=CategoryResponse)
def create(data: CategoryCreate, service: CategoryCoreDep):
    return service.create(data)


@router.put("/{category_id}", response_model=CategoryResponse)
def update(category_id: PositiveInt, data: CategoryUpdate, service: CategoryCoreDep):
    return service.update(category_id, data)


@router.delete("/{category_id}")
def delete(category_id: PositiveInt, service: CategoryCoreDep):
    return service.delete(category_id)
