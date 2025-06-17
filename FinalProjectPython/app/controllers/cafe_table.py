from fastapi import APIRouter
from typing import List
from pydantic import PositiveInt

from app.core.cafe_table import CafeTableCoreDep  # залежність сервісу столів
from app.schemas.cafe_table import CafeTableCreate, CafeTableUpdate, CafeTableResponse

router = APIRouter(
    prefix="/tables",
    tags=["Cafe Tables"]
)


@router.get("/", response_model=List[CafeTableResponse])
def get_all(service: CafeTableCoreDep):
    return service.get_all()


@router.get("/{table_id}", response_model=CafeTableResponse)
def get_by_id(table_id: PositiveInt, service: CafeTableCoreDep):
    return service.get_by_id(table_id)


@router.get("/number/{number}", response_model=CafeTableResponse)
def get_by_number(number: PositiveInt, service: CafeTableCoreDep):
    return service.get_by_number(number)

@router.get("/occupacy/{occuppied}", response_model=List[CafeTableResponse])
def get_tables_by_occupacy(occuppied: bool, service: CafeTableCoreDep):
    return service.get_tables_by_occupacy(occuppied)

@router.get("/is_occupied/{table_id}", response_model=bool)
def is_occupied(table_id: PositiveInt, service: CafeTableCoreDep):
    return service.is_table_occupied(table_id)

@router.post("/", response_model=CafeTableResponse)
def create(data: CafeTableCreate, service: CafeTableCoreDep):
    return service.create(data)


@router.put("/{table_id}", response_model=CafeTableResponse)
def update(table_id: PositiveInt, data: CafeTableUpdate, service: CafeTableCoreDep):
    return service.update(table_id, data)


@router.delete("/{table_id}")
def delete(table_id: PositiveInt, service: CafeTableCoreDep):
    return service.delete(table_id)
