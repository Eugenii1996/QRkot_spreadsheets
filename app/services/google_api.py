from copy import deepcopy
from datetime import datetime
from typing import List

from aiogoogle import Aiogoogle

from app.api.validators import check_table_values_size
from app.core.config import settings
from app.models.charity_project import CharityProject


COLUMN_COUNT = 11
COLUMN_UPDATE_FROM = 1
FORMAT = "%Y/%m/%d %H:%M:%S"
ROW_COUNT = 100
ROW_UPDATE_FROM = 1
SHEET_ID = 0
SPREADSHEET_BODY = dict(
    properties=dict(
        title='Отчет от {now_date_time}',
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=SHEET_ID,
        title='Лист1',
        gridProperties=dict(
            rowCount=ROW_COUNT,
            columnCount=COLUMN_COUNT,
        )
    ))]
)
TABLE_HEADER = [
    ['Отчет от', '{now_date_time}'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


async def spreadsheets_create(
    wrapper_services: Aiogoogle,
    spreadsheet_body=SPREADSHEET_BODY
) -> str:
    body = deepcopy(spreadsheet_body)
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    body = body['properties']['title'].format(now_date_time=now_date_time)
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: List[CharityProject],
        wrapper_services: Aiogoogle,
        table_header=TABLE_HEADER
) -> None:
    header = deepcopy(table_header)
    now_date_time = datetime.now().strftime(FORMAT)
    header[0][-1] = header[0][-1].format(now_date_time=now_date_time)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        *header,
        *([
            str(project.name),
            str(project.close_date - project.create_date),
            str(project.description)
        ] for project in projects)
    ]
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await check_table_values_size(table_values, ROW_COUNT, COLUMN_COUNT)
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f'R{ROW_UPDATE_FROM}C{COLUMN_UPDATE_FROM}:R{ROW_COUNT}C{COLUMN_COUNT}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
