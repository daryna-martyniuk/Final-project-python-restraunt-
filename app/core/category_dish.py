from typing import List, Annotated

from fastapi.params import Depends

from app.crud.category_dish import CategoryRepoDep
from app.schemas.category_dish import CategoryCreate, CategoryUpdate, CategoryResponse
from fastapi import HTTPException, status

class CategoryService:
    def __init__(self, repo: CategoryRepoDep):
        self.repo = repo

    def get_all(self) -> List[CategoryResponse]:
        categories = self.repo.get_all()
        return [CategoryResponse.model_validate(c) for c in categories]

    def get_by_id(self, category_id: int) -> CategoryResponse:
        category = self.repo.get_by_id(category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return CategoryResponse.model_validate(category)

    def get_by_name(self, name: str) -> CategoryResponse:
        category = self.repo.get_by_name(name)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return CategoryResponse.model_validate(category)

    def create(self, category_create: CategoryCreate) -> CategoryResponse:
        existing = self.repo.get_by_name(category_create.name)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category name already exists")
        category = self.repo.create(category_create)
        return CategoryResponse.model_validate(category)

    def update(self, category_id: int, category_update: CategoryUpdate) -> CategoryResponse:
        category = self.repo.get_by_id(category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        if category_update.name and category_update.name != category.name:
            if self.repo.get_by_name(category_update.name):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category name already exists")
        updated_category = self.repo.update(category_id, category_update)
        return CategoryResponse.model_validate(updated_category)

    def delete(self, category_id: int) -> bool:
        category = self.repo.get_by_id(category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        for dish in category.dishes:
            if dish.id and self.repo.has_order_items(dish.id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Cannot delete category: dish '{dish.name}' is used in orders."
                )
        self.repo.delete(category_id)
        return True

CategoryCoreDep = Annotated[CategoryService, Depends(CategoryService)]