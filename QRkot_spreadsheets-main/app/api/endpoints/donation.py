from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import Donation, User
from app.schemas.donation import DonationCreate, DonationDB, DonationDBSuper
from app.services.donation import create_donation_logic

donation_router = APIRouter()


@donation_router.post(
    '/', response_model=DonationDB,
    summary='Создать новое пожертвование')
async def create_donate(
    donation_in: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
) -> DonationDB:
    return await create_donation_logic(
        donation_in=donation_in,
        user=user,
        session=session
    )


@donation_router.get(
    '/my', response_model=list[DonationDB],
    summary='Получить пожертвования пользователя')
async def get_my_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    return await donation_crud.get_donation_user(
        user.id, session)


@donation_router.get(
    '/',
    response_model=list[DonationDBSuper],
    dependencies=[Depends(current_superuser)],
    summary='Получить все пожертвования. Доступно только суперюзерам.'
)
async def get_all_donation(
    session: AsyncSession = Depends(get_async_session)
) -> list[Donation]:
    return await donation_crud.get_multi(session)