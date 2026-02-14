from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import CharityProjectCreate

from .services import invest_funds


async def create_project_logic(
    session: AsyncSession,
    project: CharityProjectCreate
):
    await check_name_duplicate(project.name, session)

    new_project = await charity_project_crud.create(project, session)

    await invest_funds(session)

    await session.commit()
    await session.refresh(new_project)
    return new_project
