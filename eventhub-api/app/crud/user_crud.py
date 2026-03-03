from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base_crud import BaseCRUD
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserCRUD(BaseCRUD[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create_with_hash(self, db: AsyncSession, email: str, password_hash: str,
                               first_name: str, last_name: str, role: str) -> User:
        user = User(
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            role=role,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def set_active(self, db: AsyncSession, user: User, is_active: bool) -> User:
        user.is_active = is_active
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user


user_crud = UserCRUD(User)
