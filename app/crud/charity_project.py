from typing import Optional, List

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return db_project_id.scalars().first()

    async def get_closed_projects(
        self,
        session: AsyncSession,
    ) -> List[CharityProject]:
        projects = await session.execute(
            select(CharityProject).where(CharityProject.fully_invested).order_by(
                func.julianday(CharityProject.close_date) -
                func.julianday(CharityProject.create_date)
            )
        )
        return projects.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
