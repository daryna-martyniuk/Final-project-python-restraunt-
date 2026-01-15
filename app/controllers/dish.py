from fastapi import APIRouter
from typing import List
from pydantic import PositiveInt

from app.core.dish import DishCoreDep  # залежність сервісу страв
from app.schemas.dish import DishCreate, DishUpdate, DishResponse

router = APIRouter(
    prefix="/dishes",
    tags=["Dishes"]
)


@router.get("/", response_model=List[DishResponse])
def get_all(service: DishCoreDep):
    return service.get_all()


@router.get("/{dish_id}", response_model=DishResponse)
def get_by_id(dish_id: PositiveInt, service: DishCoreDep):
    return service.get_by_id(dish_id)

@router.get("/name/{dish_name}", response_model=DishResponse)
def get_by_name(dish_name: str, service: DishCoreDep):
    return service.get_by_name(dish_name)

@router.get("/category/{category_id}", response_model=List[DishResponse])
def get_by_category_id(category_id: PositiveInt, service: DishCoreDep):
    return service.get_dishes_by_category_id(category_id)

@router.get("/on_promotion/", response_model=List[DishResponse])
def get_dishes_on_promotion(service: DishCoreDep):
    return service.get_dishes_on_promotion()

@router.get("/most_popular/", response_model=DishResponse)
def get_most_popular_dish(service: DishCoreDep):
    return service.get_most_popular_dish()

@router.get("/sort/{ascending}", response_model=List[DishResponse])
def sort_dishes_by_price(ascending: bool, service: DishCoreDep):
    return service.sort_dishes_by_price(ascending)
@router.post("/", response_model=DishResponse)
def create(data: DishCreate, service: DishCoreDep):
    return service.create(data)


@router.put("/{dish_id}", response_model=DishResponse)
def update(dish_id: PositiveInt, data: DishUpdate, service: DishCoreDep):
    return service.update(dish_id, data)


@router.delete("/{dish_id}")
def delete(dish_id: PositiveInt, service: DishCoreDep):
    return service.delete(dish_id)
