from fastapi.params import Depends
from sqlalchemy import select, func
from typing import Annotated

from sqlalchemy.orm import joinedload

from app.db import SessionContext
from app.models.models import Dish, PromotionDishAssociation, OrderItem
from app.schemas.dish import DishCreate, DishUpdate


class DishRepo:
    def __init__(self, db: SessionContext):
        self.db = db

    def get_all(self) -> list[Dish]:
        stmt = select(Dish)
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_by_id(self, dish_id: int) -> Dish | None:
        stmt = select(Dish).where(Dish.id == dish_id)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def get_by_name(self, dish_name: str) -> Dish | None:
        stmt = select(Dish).where(func.lower(Dish.name).contains(dish_name.lower()))
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def get_dishes_by_category(self, category_id: int) -> list[Dish]:
        stmt = select(Dish).where(Dish.category_id == category_id)
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_dishes_on_promotion(self) -> list[Dish]:
        stmt = (
            select(Dish)
            .join(PromotionDishAssociation, Dish.id == PromotionDishAssociation.dish_id)
            .options(joinedload(Dish.category))
            .distinct()
        )
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_most_popular_dish(self) -> Dish | None:
        stmt = (
            select(Dish)
            .join(OrderItem, Dish.id == OrderItem.dish_id)
            .group_by(Dish.id)
            .order_by(func.sum(OrderItem.quantity).desc())
            .limit(1)
        )
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def sort_dishes_by_price(self, ascending: bool = True) -> list[Dish]:
        stmt = select(Dish).order_by(Dish.price.asc() if ascending else Dish.price.desc())
        result = self.db.execute(stmt)
        return result.scalars().all()

    def create(self, data: DishCreate) -> Dish:
        dish = Dish(**data.model_dump())
        self.db.add(dish)
        self.db.commit()
        self.db.refresh(dish)
        return dish

    def update(self, dish_id: int, data: DishUpdate) -> Dish | None:
        dish = self.get_by_id(dish_id)
        if not dish:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(dish, key, value)
        self.db.commit()
        self.db.refresh(dish)
        return dish

    def delete(self, dish_id: int) -> bool:
        dish = self.get_by_id(dish_id)
        if not dish:
            return False
        self.db.delete(dish)
        self.db.commit()
        return True

    def has_order_items(self, dish_id: int) -> bool:
        return self.db.query(OrderItem).filter(OrderItem.dish_id == dish_id).first() is not None

    def delet
DishRepoDep = Annotated[DishRepo, Depends(DishRepo)]
