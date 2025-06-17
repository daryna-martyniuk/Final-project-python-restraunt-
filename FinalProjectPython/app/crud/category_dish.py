from fastapi.params import Depends
from sqlalchemy import select, func
from typing import Annotated
from app.db import SessionContext
from app.models.models import DishCategory, OrderItem
from app.schemas.category_dish import CategoryCreate, CategoryUpdate


class CategoryRepo:
    def __init__(self, db: SessionContext):
        self.db = db

    def get_all(self) -> list[DishCategory]:
        stmt = select(DishCategory)
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_by_id(self, category_id: int) -> DishCategory | None:
        stmt = select(DishCategory).where(DishCategory.id == category_id)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def get_by_name(self, category_name: str) -> DishCategory | None:
        stmt = select(DishCategory).where(func.lower(DishCategory.name).contains(category_name.lower()))
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def create(self, data: CategoryCreate) -> DishCategory:
        category = DishCategory(**data.model_dump())
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update(self, category_id: int, data: CategoryUpdate) -> DishCategory | None:
        category = self.get_by_id(category_id)
        if not category:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(category, key, value)
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category_id: int) -> bool:
        category = self.get_by_id(category_id)
        if not category:
            return False
        self.db.delete(category)
        self.db.commit()
        return True

    def has_order_items(self, dish_id: int) -> bool:
        stmt = select(OrderItem).where(OrderItem.dish_id == dish_id)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none() is not None

CategoryRepoDep = Annotated[CategoryRepo, Depends(CategoryRepo)]