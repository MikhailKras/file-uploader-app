import csv
import os
from io import BytesIO

from fastapi import UploadFile
from httpx import AsyncClient


async def test_upload_file_success(ac: AsyncClient):
    sample_csv_content = "column1,column2\nvalue1,value2\n"
    sample_csv_content = sample_csv_content.encode("utf-8")
    sample_csv_file = UploadFile(filename="sample.csv", file=BytesIO(sample_csv_content))
    response = await ac.post("/upload_file", files={"file": (sample_csv_file.filename, sample_csv_file.file)})

    assert response.status_code == 201
    file_path = os.path.join("datasets", sample_csv_file.filename)
    assert os.path.exists(file_path)
    if os.path.exists(file_path):
        os.remove(file_path)


async def test_upload_file_duplicat(ac: AsyncClient):
    sample_csv_content = "column1,column2\nvalue1,value2\n"
    file_path = os.path.join("datasets", "sample.csv")
    with open(file_path, "w", newline='') as f:
        csv_writer = csv.writer(f)
        for line in sample_csv_content.split('\n'):
            if line:
                csv_writer.writerow(line.split(','))

    sample_csv_content = sample_csv_content.encode("utf-8")
    sample_csv_file = UploadFile(filename="sample.csv", file=BytesIO(sample_csv_content))
    response = await ac.post("/upload_file", files={"file": (sample_csv_file.filename, sample_csv_file.file)})
    assert response.status_code == 400
    assert response.json()["detail"] == f"File '{sample_csv_file.filename}' already exists"
    os.remove(file_path)


async def test_upload_file_not_csv(ac: AsyncClient):
    sample_text_content = "text content"
    sample_text_content = sample_text_content.encode("utf-8")
    sample_text_file = UploadFile(filename="sample.txt", file=BytesIO(sample_text_content))
    response = await ac.post("/upload_file", files={"file": (sample_text_file.filename, sample_text_file.file)})
    assert response.status_code == 400
    assert response.json()["detail"] == "File must be a CSV file."


async def test_get_file_info(ac: AsyncClient):
    response = await ac.get("/files")
    assert response.status_code == 200
    assert response.json()["files"]
