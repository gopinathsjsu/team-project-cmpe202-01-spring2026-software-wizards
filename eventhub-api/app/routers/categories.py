from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import require_role
from app.schemas.category import CategoryCreate, CategoryRead
from app.crud.category_crud import category_crud

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=List[CategoryRead])
async def list_categories(db: AsyncSession = Depends(get_db)):
    return await category_crud.get_multi(db, limit=100)


@router.get("/{id}", response_model=CategoryRead)
async def get_category(id: str, db: AsyncSession = Depends(get_db)):
    from uuid import UUID
    cat = await category_crud.get(db, UUID(id))
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return cat


@router.post("", response_model=CategoryRead, status_code=201,
             dependencies=[Depends(require_role("admin"))])
async def create_category(data: CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await category_crud.create(db, data)