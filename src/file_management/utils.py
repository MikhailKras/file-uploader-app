from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.file_management.models import file_info
from src.file_management.schemas import FileInfoInDB


async def get_all_file_info_db(
        session: AsyncSession = Depends(get_async_session)
) -> List[FileInfoInDB]:
    column_names = [column.name for column in file_info.columns]
    select_query = (select(file_info))
    result = await session.execute(select_query)
    file_info_in_db = result.fetchall()
    file_info_in_db_with_column_names = [{column_name: value for column_name, value in zip(column_names, row)} for row in file_info_in_db]
    return [FileInfoInDB(**file_info_row) for file_info_row in file_info_in_db_with_column_names]
