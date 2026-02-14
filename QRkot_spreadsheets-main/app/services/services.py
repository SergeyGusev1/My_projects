from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.models.donation import Donation


def finalize_investment(obj: Union[CharityProject, Donation]) -> None:
    """Проверяет завершены ли инвестиции в объекте."""
    if obj.invested_amount == obj.full_amount:
        obj.fully_invested = True
        obj.close_date = datetime.now()


async def invest_funds(
    session: AsyncSession
) -> None:
    """Распределяет средства между активными проектами и пожертвованиями."""
    projects = await charity_project_crud.get_not_fully_invested(session)
    donations = await donation_crud.get_not_fully_invested(session)
    for project in projects:
        if project.fully_invested:
            continue
        for donation in donations:
            if donation.fully_invested:
                continue

            project_invested = (project.invested_amount
                                if project.invested_amount is not None else 0)
            donation_invested = (donation.invested_amount
                                 if donation.invested_amount
                                 is not None else 0)

            need = project.full_amount - project_invested
            remain = donation.full_amount - donation_invested
            to_invest = min(need, remain)

            if to_invest <= 0:
                continue
            project.invested_amount = project_invested + to_invest
            donation.invested_amount = donation_invested + to_invest

            finalize_investment(project)
            finalize_investment(donation)

            session.add(project)
            session.add(donation)
