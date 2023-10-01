import csv
import json
import os
from typing import List, Optional

import pandas as pd
from fastapi import APIRouter, UploadFile, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.file_management.models import file_info
from src.file_management.schemas import FileInfoInDB, SortOrderEnum
from src.file_management.utils import get_all_file_info_db, get_file_db

router = APIRouter()


@router.post("/upload_file", response_class=JSONResponse)
async def upload_file(file: UploadFile, session: AsyncSession = Depends(get_async_session)):
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File must be a CSV file.")

    if os.path.exists(f"datasets/{file.filename}"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"File '{file.filename}' already exists")

    file_path = os.path.join("datasets", file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        column_names = reader.fieldnames

    insert_query = insert(file_info).values(
        file_name=file.filename,
        column_names=column_names
    )

    await session.execute(insert_query)
    await session.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "File uploaded successfully."})


@router.get("/files")
async def get_file_info(session: AsyncSession = Depends(get_async_session)):
    files: List[FileInfoInDB] = await get_all_file_info_db(session=session)
    files_data = {
        "files": [
            {
                "id": files[x].id,
                "file_name": files[x].file_name,
                "uploaded_time": str(files[x].uploaded_time),
                "column_names": files[x].column_names,
            }
            for x in range(len(files))
        ]
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=files_data)


@router.post("/fetch_data")
async def fetch_data(
        file_name: str = None,
        file_id: int = None,
        session: AsyncSession = Depends(get_async_session),
        sort_by: List[str] | None = None,
        sort_orders: List[SortOrderEnum] | None = None,
        filter_by: List[str] | None = None,
        filter_values: List[str] | None = None
):
    if not file_name and not file_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Either 'file_id' or 'file_name' is required.")
    if file_id and file_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only one of 'file_id' or 'file_name' can be provided.")
    if sort_by and sort_orders and len(sort_by) != len(sort_orders):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Number of sort orders must match number of sort columns.")
    if filter_by and filter_values and len(filter_by) != len(filter_values):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Number of filter values must match number of filter columns.")

    file: Optional[FileInfoInDB] = await get_file_db(file_name=file_name, file_id=file_id, session=session)
    if file is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")

    file_path = f"datasets/{file.file_name}"
    df = pd.read_csv(file_path)

    if sort_by:
        try:
            df = df.sort_values(by=sort_by, ascending=[True if sort_order == "asc" else False for sort_order in sort_orders])
        except KeyError as e:
            invalid_column_name = str(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid sort column name: {invalid_column_name}")

    if filter_by and filter_values:
        for column, filter_value in zip(filter_by, filter_values):
            try:
                df = df[df[column].str.contains(filter_value)]
            except KeyError:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid filter column name: {column}")
    df_json = df.to_json(orient="records", index=False)
    data = json.loads(df_json)
    json_string = json.dumps(data, ensure_ascii=False)
    return JSONResponse(status_code=status.HTTP_200_OK, content=json_string)


@router.delete('/delete_file', response_class=JSONResponse)
async def delete_file(
        file_name: str = None,
        file_id: int = None,
        session: AsyncSession = Depends(get_async_session),
):
    if not file_name and not file_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Either 'file_id' or 'file_name' is required.")
    if file_id and file_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only one of 'file_id' or 'file_name' can be provided.")

    file: Optional[FileInfoInDB] = await get_file_db(file_name=file_name, file_id=file_id, session=session)
    if file is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")
    delete_query = delete(file_info).where(file_info.c.id == file.id)
    await session.execute(delete_query)
    await session.commit()

    file_path = f"datasets/{file.file_name}"
    os.remove(file_path)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "File deleted successfully."})
