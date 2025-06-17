from fastapi import APIRouter
from typing import List
from pydantic import PositiveInt

from app.core.promotion import PromotionCoreDep
from app.schemas.promotion import PromotionCreate, PromotionUpdate, PromotionResponse

router = APIRouter(
    prefix="/promotions",
    tags=["Promotions"]
)


@router.get("/", response_model=List[PromotionResponse])
def get_all(service: PromotionCoreDep):
    return service.get_all()

@router.get("/active/", response_model=List[PromotionResponse])
def get_active_promotion(service: PromotionCoreDep):
    return service.get_active_promotion()
@router.get("/{promotion_id}", response_model=PromotionResponse)
def get_by_id(promotion_id: PositiveInt, service: PromotionCoreDep):
    return service.get_by_id(promotion_id)

@router.post("/", response_model=PromotionResponse)
def create(data: PromotionCreate, service: PromotionCoreDep):
    return service.create(data)


@router.put("/{promotion_id}", response_model=PromotionResponse)
def update(promotion_id: PositiveInt, data: PromotionUpdate, service: PromotionCoreDep):
    return service.update(promotion_id, data)


@router.delete("/{promotion_id}")
def delete(promotion_id: PositiveInt, service: PromotionCoreDep):
    return service.delete(promotion_id)
