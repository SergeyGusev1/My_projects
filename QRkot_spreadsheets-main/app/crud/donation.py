from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCharityRepository
from app.models import Donation
from app.schemas.donation import DonationCreate, DonationUpdate


class CRUDDonation(
    BaseCharityRepository[
        Donation, DonationCreate, DonationUpdate]
):
    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        project_id = await session.execute(
            select(Donation.id).where(
                Donation.name == project_name
            )
        )
        return project_id.scalars().first()

    async def get_donation_user(
        self,
        user_id: int,
        session: AsyncSession
    ) -> Optional[list[Donation]]:
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user_id
            )
        )

        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
