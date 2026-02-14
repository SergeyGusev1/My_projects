from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_project_exists(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Проверка наличия проекта."""
    project = await session.get(CharityProject, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    return project


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession
) -> None:
    """Проверка дубликата имени проекта."""
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name,
        session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Not unique name'
        )


def check_project_not_closed(project):
    """Проверка закрыт ли проект."""
    if project.fully_invested:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail="Нельзя менять закрытый проект")


def check_full_amount_valid(new_amount, invested_amount):
    """Проверка при изменении, чтобы сумма не была меньше внесённой."""
    if new_amount is not None and new_amount < invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Новая сумма должна быть не меньше внесённой"
        )


def check_project_no_invested_funds(project):
    """Проверка проекта при удалении, чтобы в нём не было внесённых средств."""
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Нельзя удалить проект, в который уже внесли средства"
        )
