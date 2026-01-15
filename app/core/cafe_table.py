from typing import List, Annotated, Optional

from fastapi.params import Depends
from fastapi import HTTPException, status

from app.crud.cafe_table import CafeTableRepoDep
from app.schemas.cafe_table import CafeTableCreate, CafeTableUpdate, CafeTableResponse


class CafeTableService:
    def __init__(self, repo: CafeTableRepoDep):
        self.repo = repo

    def get_all(self) -> List[CafeTableResponse]:
        tables = self.repo.get_all()
        return [CafeTableResponse.model_validate(t) for t in tables]

    def get_by_id(self, table_id: int) -> CafeTableResponse:
        table = self.repo.get_by_id(table_id)
        if not table:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
        return CafeTableResponse.model_validate(table)

    def get_by_number(self, number: int) -> CafeTableResponse:
        table = self.repo.get_by_number(number)
        if not table:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
        return CafeTableResponse.model_validate(table)

    def get_tables_by_occupacy(self, occupied: bool) -> List[CafeTableResponse]:
        tables = self.repo.get_tables_by_occupacy(occupied)
        if not tables:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tables not found")
        return [CafeTableResponse.model_validate(t) for t in tables]

    def is_table_occupied(self, table_id: int) -> bool:
        table = self.repo.get_by_id(table_id)
        if not table:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
        is_occupied = self.repo.is_table_occupied(table.id)
        return is_occupied

    def create(self, table_create: CafeTableCreate) -> CafeTableResponse:
        existing = self.repo.get_by_number(table_create.number)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Table number already exists")
        table = self.repo.create(table_create)
        return CafeTableResponse.model_validate(table)

    def update(self, table_id: int, table_update: CafeTableUpdate) -> CafeTableResponse:
        table = self.repo.get_by_id(table_id)
        if not table:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
        if table_update.number is not None and table_update.number != table.number:
            if self.repo.get_by_number(table_update.number):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Table number already exists")
        updated_table = self.repo.update(table_id, table_update)
        return CafeTableResponse.model_validate(updated_table)

    def delete(self, table_id: int) -> bool:
        table = self.repo.get_by_id(table_id)
        if not table:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
        if self.repo.is_table_occupied(table.id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Table occupied already")

        self.repo.delete(table_id)
        return True


CafeTableCoreDep = Annotated[CafeTableService, Depends(CafeTableService)]
