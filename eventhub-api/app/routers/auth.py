import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.crud.user_crud import user_crud
from app.models.registration import PasswordResetToken
from app.schemas.user import (
    UserCreate, TokenResponse, AccessTokenResponse,
    LoginRequest, RefreshRequest, PasswordResetRequest, PasswordResetConfirm,
)
from app.services.auth_service import auth_service
from app.config import get_settings

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await user_crud.get_by_email(db, data.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    password_hash = auth_service.hash_password(data.password)
    user = await user_crud.create_with_hash(
        db,
        email=data.email,
        password_hash=password_hash,
        first_name=data.first_name,
        last_name=data.last_name,
        role=data.role,
    )
    access_token = auth_service.create_access_token(user.id, user.role)
    refresh_token = auth_service.create_refresh_token(user.id)
    from app.schemas.user import UserRead
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserRead.model_validate(user),
    )


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_by_email(db, data.email)
    if not user or not auth_service.verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account suspended")

    access_token = auth_service.create_access_token(user.id, user.role)
    refresh_token = auth_service.create_refresh_token(user.id)
    from app.schemas.user import UserRead
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserRead.model_validate(user),
    )


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh_token(data: RefreshRequest, db: AsyncSession = Depends(get_db)):
    payload = auth_service.verify_token(data.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = await user_crud.get(db, uuid.UUID(payload["sub"]))
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token = auth_service.create_access_token(user.id, user.role)
    return AccessTokenResponse(access_token=access_token)


@router.post("/request-password-reset", status_code=200)
async def request_password_reset(data: PasswordResetRequest, db: AsyncSession = Depends(get_db)):
    """Always returns 200 to avoid revealing whether an email exists."""
    import asyncio
    user = await user_crud.get_by_email(db, data.email)
    if user:
        import secrets
        token_str = secrets.token_urlsafe(32)
        expires = datetime.now(timezone.utc) + timedelta(hours=1)
        token = PasswordResetToken(
            user_id=user.id,
            token=token_str,
            expires_at=expires,
            created_at=datetime.now(timezone.utc),
        )
        db.add(token)
        await db.commit()

        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token_str}"
        from app.services.notification_service import NotificationFactory, NotificationType
        from app.services.email_service import email_service
        notif = NotificationFactory.create(
            NotificationType.PASSWORD_RESET,
            user=user,
            reset_link=reset_link,
        )
        asyncio.create_task(email_service.send(notif))

    return {"message": "If that email is registered, you will receive a reset link."}


@router.post("/reset-password", status_code=200)
async def reset_password(data: PasswordResetConfirm, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    result = await db.execute(
        select(PasswordResetToken).where(PasswordResetToken.token == data.token)
    )
    token_obj = result.scalar_one_or_none()

    if not token_obj:
        raise HTTPException(status_code=404, detail="Token not found")
    if token_obj.used:
        raise HTTPException(status_code=400, detail="Token already used")
    if token_obj.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Token expired")

    user = await user_crud.get(db, token_obj.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password_hash = auth_service.hash_password(data.new_password)
    token_obj.used = True
    db.add(user)
    db.add(token_obj)
    await db.commit()
    return {"message": "Password reset successfully"}
