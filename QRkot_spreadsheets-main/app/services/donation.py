from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB
from app.services.services import invest_funds


async def create_donation_logic(
    donation_in: DonationCreate,
    user: User,
    session: AsyncSession
) -> DonationDB:
    new_donation = await donation_crud.create(
        obj_in=donation_in,
        session=session,
        user=user
    )
    await invest_funds(session)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation