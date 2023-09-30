import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel


class FileInfoInDB(BaseModel):
    id: int
    file_name: str
    uploaded_time: datetime.datetime
    column_names: List[str]


class SortOrderEnum(str, Enum):
    asc = "asc"
    desc = "desc"


class FileQueryParams(BaseModel):
    file_id: int = None
    file_name: str = None
    sort_by: str = None
    sort_order: SortOrderEnum = SortOrderEnum.asc
    filter_by: str = None
    filter_value: str = None
