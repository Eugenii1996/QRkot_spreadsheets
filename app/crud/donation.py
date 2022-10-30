from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation


class CRUDDonation(CRUDBase):

    async def get_by_user(
            self,
            session: AsyncSession,
            user_id: int
    ):
        donations = await session.execute(
            select(Donation).where(Donation.user_id == user_id))
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
