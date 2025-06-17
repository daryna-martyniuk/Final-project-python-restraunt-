from typing import List
from fastapi import HTTPException, status
from fastapi.params import Depends
from typing import Annotated

from unicodedata import category

from app.crud.dish import DishRepoDep
from app.crud.category_dish import CategoryRepoDep
from app.models import Dish
from app.schemas.dish import DishCreate, DishUpdate, DishResponse

class DishService:
    def __init__(self, dish_repo: DishRepoDep, category_repo: CategoryRepoDep):
        self.dish_repo = dish_repo
        self.category_repo = category_repo

    def get_all(self) -> List[DishResponse]:
        dishes = self.dish_repo.get_all()
        return [DishResponse.model_validate(d) for d in dishes]

    def get_by_id(self, dish_id: int) -> DishResponse:
        dish = self.dish_repo.get_by_id(dish_id)
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")
        return DishResponse.model_validate(dish)

    def get_by_name(self, name: str) -> DishResponse:
        dish = self.dish_repo.get_by_name(name)
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")
        return DishResponse.model_validate(dish)

    def get_dishes_by_category_id(self, category_id: int) -> List[DishResponse]:
        category = self.category_repo.get_by_id(category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        dishes = self.dish_repo.get_dishes_by_category(category_id)
        if not dishes:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dishes not found")
        return [DishResponse.model_validate(d) for d in dishes]

    def get_dishes_on_promotion(self) -> List[DishResponse]:
        dishes = self.dish_repo.get_dishes_on_promotion()
        if not dishes:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")
        return [DishResponse.model_validate(d) for d in dishes]

    def get_most_popular_dish(self) -> DishResponse:
        dish = self.dish_repo.get_most_popular_dish()
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")
        return DishResponse.model_validate(dish)

    def sort_dishes_by_price(self, ascending: bool = True) -> List[DishResponse]:
        dishes = self.dish_repo.sort_dishes_by_price(ascending)
        if not dishes:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")
        return [DishResponse.model_validate(d) for d in dishes]



    def create(self, dish_create: DishCreate) -> DishResponse:
        category = self.category_repo.get_by_id(dish_create.category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category does not exist")

        if dish_create.price <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Price must be greater than 0")

        existing = self.dish_repo.get_by_name(dish_create.name)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dish name already exists")

        dish = self.dish_repo.create(dish_create)
        return DishResponse.model_validate(dish)

    def update(self, dish_id: int, dish_update: DishUpdate) -> DishResponse:
        dish = self.dish_repo.get_by_id(dish_id)
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")

        if dish_update.category_id:
            category = self.category_repo.get_by_id(dish_update.category_id)
            if not category:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category does not exist")

        if dish_update.name and dish_update.name != dish.name:
            if self.dish_repo.get_by_name(dish_update.name):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dish name already exists")

        if dish_update.price <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Price must be greater than 0")

        updated_dish = self.dish_repo.update(dish_id, dish_update)
        return DishResponse.model_validate(updated_dish)

    def delete(self, dish_id: int) -> bool:
        dish = self.dish_repo.get_by_id(dish_id)
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")
        if self.dish_repo.has_order_items(dish_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dish is in order")
        self.dish_repo.delete(dish_id)
        return True

DishCoreDep = Annotated[DishService, Depends(DishService)]