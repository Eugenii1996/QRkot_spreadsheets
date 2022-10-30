from copy import deepcopy
from datetime import datetime
from typing import List

from aiogoogle import Aiogoogle

from app.services.validators import check_table_values_size
from app.core.config import settings
from app.models.charity_project import CharityProject


COLUMN_COUNT = 11
FORMAT = "%Y/%m/%d %H:%M:%S"
ROW_COUNT = 100
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
    spreadsheet_body=None
) -> str:
    if spreadsheet_body is None:
        spreadsheet_body = deepcopy(SPREADSHEET_BODY)
        now_date_time = datetime.now().strftime(FORMAT)
        spreadsheet_body['properties']['title'] = str(now_date_time)
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: List[CharityProject],
        wrapper_services: Aiogoogle,
        table_header=None
) -> None:
    if table_header is None:
        table_header = deepcopy(TABLE_HEADER)
        now_date_time = datetime.now().strftime(FORMAT)
        table_header[0][-1] = str(now_date_time)
    table_values = [
        *table_header,
        *([
            str(project.name),
            str(project.close_date - project.create_date),
            str(project.description)
        ] for project in projects)
    ]
    service = await wrapper_services.discover('sheets', 'v4')
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    table_values_rows_count = len(table_values)
    table_values_columns_count = len(max(table_values, key=len))
    check_table_values_size(
        table_values_rows_count,
        table_values_columns_count,
        ROW_COUNT,
        COLUMN_COUNT
    )
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=(
                f'R1C1:R{table_values_rows_count}'
                f'C{table_values_columns_count}'
            ),
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
