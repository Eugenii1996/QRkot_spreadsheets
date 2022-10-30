from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation


async def investing(
    new_object: Union[CharityProject, Donation],
    session: AsyncSession,
) -> Union[CharityProject, Donation]:
    if new_object.invested_amount is None:
        new_object.invested_amount = 0
    crud_model = (
        donation_crud
        if isinstance(new_object, CharityProject)
        else charity_project_crud
    )
    all_changed_objects = []
    for model_object in await crud_model.get_not_fully_invested(session):
        free_amount = (
            min(
                (model_object.full_amount - model_object.invested_amount),
                (new_object.full_amount - new_object.invested_amount)
            )
        )

        def change_invested_amount(object):
            object.invested_amount += free_amount
            if object.invested_amount == object.full_amount:
                object.fully_invested, object.close_date = True, datetime.now()

        change_invested_amount(model_object)
        change_invested_amount(new_object)
        all_changed_objects.append(model_object)
        if new_object.fully_invested:
            break
    return all_changed_objects
