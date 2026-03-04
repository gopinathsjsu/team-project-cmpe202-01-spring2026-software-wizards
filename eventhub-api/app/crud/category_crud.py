from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base_crud import BaseCRUD
from app.models.category import Category
from app.schemas.category import CategoryCreate


class CategoryCRUD(BaseCRUD[Category, CategoryCreate, CategoryCreate]):

    async def get_by_slug(self, db: AsyncSession, slug: str) -> Optional[Category]:
        result = await db.execute(select(Category).where(Category.slug == slug))
        return result.scalar_one_or_none()


category_crud = CategoryCRUD(Category)