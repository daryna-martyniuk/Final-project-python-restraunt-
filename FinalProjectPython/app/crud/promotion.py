from datetime import datetime
from operator import or_

from fastapi.params import Depends
from sqlalchemy import select, and_
from typing import Annotated

from app.db import SessionContext
from app.models.models import Promotion, Dish
from app.schemas.promotion import PromotionCreate, PromotionUpdate


class PromotionRepo:
    def __init__(self, db: SessionContext):
        self.db = db

    def get_all(self) -> list[Promotion]:
        stmt = select(Promotion)
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_by_id(self, promotion_id: int) -> Promotion | None:
        stmt = select(Promotion).where(Promotion.id == promotion_id)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()


    def get_active_promotion(self) -> list[Promotion]:
        now = datetime.utcnow()
        today = now.date()
        current_time = now.time()

        stmt = select(Promotion).where(
            Promotion.valid_from <= today,
            Promotion.valid_to >= today,
            or_(Promotion.start_time == None, Promotion.start_time <= current_time),
            or_(Promotion.end_time == None, Promotion.end_time >= current_time),
        )
        result = self.db.execute(stmt)
        return result.scalars().all()

    def create(self, data: PromotionCreate) -> Promotion:
        promotion = Promotion(
            description=data.description,
            discount_percent=data.discount_percent,
            valid_from=data.valid_from,
            valid_to=data.valid_to,
            start_time=data.start_time,
            end_time=data.end_time
        )

        if data.dish_ids:
            stmt = select(Dish).where(Dish.id.in_(data.dish_ids))
            result = self.db.execute(stmt)
            dishes = result.scalars().all()
            promotion.dishes = dishes

        self.db.add(promotion)
        self.db.commit()
        self.db.refresh(promotion)
        return promotion

    def update(self, promotion_id: int, data: PromotionUpdate) -> Promotion | None:
        promotion = self.get_by_id(promotion_id)
        if not promotion:
            return None
        for key, value in data.model_dump(exclude_unset=True, exclude={"dish_ids"}).items():
            setattr(promotion, key, value)

        if data.dish_ids is not None:
            stmt = select(Dish).where(Dish.id.in_(data.dish_ids))
            result = self.db.execute(stmt)
            promotion.dishes = result.scalars().all()

        self.db.commit()
        self.db.refresh(promotion)
        return promotion

    def delete(self, promotion_id: int) -> bool:
        promotion = self.get_by_id(promotion_id)
        if not promotion:
            return False
        self.db.delete(promotion)
        self.db.commit()
        return True

PromotionRepoDep = Annotated[PromotionRepo, Depends(PromotionRepo)]