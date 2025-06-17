from typing import List
from fastapi import HTTPException, status
from fastapi.params import Depends
from typing import Annotated

from app.crud.promotion import PromotionRepoDep
from app.crud.dish import DishRepoDep
from app.schemas.promotion import PromotionCreate, PromotionUpdate, PromotionResponse


class PromotionService:
    def __init__(self, promotion_repo: PromotionRepoDep, dish_repo: DishRepoDep):
        self.promotion_repo = promotion_repo
        self.dish_repo = dish_repo

    def get_all(self) -> List[PromotionResponse]:
        promotions = self.promotion_repo.get_all()
        return [PromotionResponse.model_validate(p) for p in promotions]

    def get_by_id(self, promotion_id: int) -> PromotionResponse:
        promotion = self.promotion_repo.get_by_id(promotion_id)
        if not promotion:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")
        return PromotionResponse.model_validate(promotion)

    def get_active_promotion(self) -> List[PromotionResponse]:
        promotions = self.promotion_repo.get_active_promotion()
        if not promotions:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")
        return [PromotionResponse.model_validate(p) for p in promotions]

    def create(self, promotion_create: PromotionCreate) -> PromotionResponse:
        if promotion_create.valid_from > promotion_create.valid_to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="valid_from cannot be after valid_to"
            )

        if promotion_create.start_time and promotion_create.end_time:
            if promotion_create.start_time > promotion_create.end_time:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="start_time cannot be after end_time"
                )

        for dish_id in promotion_create.dish_ids:
            if not self.dish_repo.get_by_id(dish_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Dish id {dish_id} does not exist"
                )

        created = self.promotion_repo.create(promotion_create)
        return PromotionResponse.model_validate(created)

    def update(self, promotion_id: int, promotion_update: PromotionUpdate) -> PromotionResponse:
        promotion = self.promotion_repo.get_by_id(promotion_id)
        if not promotion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Promotion not found"
            )

        # Перевірка дат
        if promotion_update.valid_from and promotion_update.valid_to:
            if promotion_update.valid_from > promotion_update.valid_to:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="valid_from cannot be after valid_to"
                )

        # Перевірка часу
        if promotion_update.start_time and promotion_update.end_time:
            if promotion_update.start_time > promotion_update.end_time:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="start_time cannot be after end_time"
                )

        # Перевірка dish_ids, якщо оновлюються
        if promotion_update.dish_ids is not None:
            for dish_id in promotion_update.dish_ids:
                if not self.dish_repo.get_by_id(dish_id):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Dish id {dish_id} does not exist"
                    )

        updated = self.promotion_repo.update(promotion_id, promotion_update)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Promotion not found after update"
            )

        return PromotionResponse.model_validate(updated)

    def delete(self, promotion_id: int) -> bool:
        promotion = self.promotion_repo.get_by_id(promotion_id)
        if not promotion:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")
        self.promotion_repo.delete(promotion_id)
        return True


PromotionCoreDep = Annotated[PromotionService, Depends(PromotionService)]
