from fastapi.params import Depends
from sqlalchemy import select, exists
from typing import Annotated

from app.db import SessionContext
from app.models.models import CafeTable, Order
from app.schemas.cafe_table import CafeTableCreate, CafeTableUpdate


class CafeTableRepo:
    def __init__(self, db: SessionContext):
        self.db = db

    def get_all(self) -> list[CafeTable]:
        stmt = select(CafeTable)
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_by_id(self, table_id: int) -> CafeTable | None:
        stmt = select(CafeTable).where(CafeTable.id == table_id)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def get_by_number(self, number: int) -> CafeTable | None:
        stmt = select(CafeTable).where(CafeTable.number == number)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def get_tables_by_occupacy(self, occupied: bool) -> list[CafeTable]:
        subquery = select(Order.id).where(
            Order.table_id == CafeTable.id,
            Order.is_completed == False
        )

        if occupied:
            stmt = select(CafeTable).where(exists(subquery))
        else:
            stmt = select(CafeTable).where(~exists(subquery))

        result = self.db.execute(stmt)
        return result.scalars().all()

    def is_table_occupied(self, table_id: int) -> bool:
        stmt = select(Order).where(
            Order.table_id == table_id,
            Order.is_completed == False
        )
        result = self.db.execute(stmt)
        return result.first() is not None  # Повертає True, якщо існує активне замовлення

    def create(self, data: CafeTableCreate) -> CafeTable:
        table = CafeTable(**data.model_dump())
        self.db.add(table)
        self.db.commit()
        self.db.refresh(table)
        return table

    def update(self, table_id: int, data: CafeTableUpdate) -> CafeTable | None:
        table = self.get_by_id(table_id)
        if not table:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(table, key, value)
        self.db.commit()
        self.db.refresh(table)
        return table

    def delete(self, table_id: int) -> bool:
        table = self.get_by_id(table_id)
        if not table:
            return False
        self.db.delete(table)
        self.db.commit()
        return True


CafeTableRepoDep = Annotated[CafeTableRepo, Depends(CafeTableRepo)]
