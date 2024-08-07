from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models import CharityProject
from app.services import constants as const


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(const.FORMAT)
    service = await wrapper_services.discover(const.GOOGLE_SHEETS, const.VERSION_4)
    spreadsheet_body = {
        'properties': {'title': f'Отчёт от {now_date_time}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': const.SHEET_TYPE,
                                   'sheetId': 0,
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': 100,
                                                      'columnCount': 11}}}]
    }
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
    service = await wrapper_services.discover(const.GOOGLE_DRIVE, const.VERSION_3)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        closed_projects: list[CharityProject],
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover(const.GOOGLE_SHEETS, const.VERSION_4)
    await set_user_permissions(spreadsheetid=spreadsheetid,
                               wrapper_services=wrapper_services)
    table_values = const.TABLE_TITLES
    for project in closed_projects:
        table_values.append([
            project.name,
            str(project.close_date - project.create_date),
            project.description
        ])
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
