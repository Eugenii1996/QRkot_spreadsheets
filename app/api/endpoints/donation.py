from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import (
    DonationCreate, DonationDB, DonationAdminDB
)
from app.services.investing import investing


router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
)
async def create_new_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Для авторизованных пользователей."""
    donation = await donation_crud.create(donation, session, user)
    investing_objects = await investing(donation, session)
    session.add(donation)
    if investing_objects:
        session.add_all(investing_objects)
    await session.commit()
    await session.refresh(donation)
    return donation


@router.get(
    '/',
    response_model=List[DonationAdminDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Для авторизованных пользователей."""
    return await donation_crud.get_by_user(session, user.id)
