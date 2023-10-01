import os
from io import BytesIO

from fastapi import UploadFile
from httpx import AsyncClient


async def test_integration_file_management(ac: AsyncClient):
    sample_csv_content = "strings,ints\nd,1\nc,2\nb,3\na,4"
    sample_csv_content = sample_csv_content.encode("utf-8")
    sample_csv_file = UploadFile(filename="sample.csv", file=BytesIO(sample_csv_content))
    response = await ac.post("/upload_file", files={"file": (sample_csv_file.filename, sample_csv_file.file)})
    assert response.status_code == 201
    file_path = os.path.join("datasets", sample_csv_file.filename)
    assert os.path.exists(file_path)

    response = await ac.get("/files")
    assert response.status_code == 200

    response = await ac.post("/fetch_data", params={"file_id": 1}, json={"sort_by": ["ints"], "sort_orders": ["desc"]})
    assert response.status_code == 200
    assert response.json() == (
        '[{"strings": "a", "ints": 4},'
        ' {"strings": "b", "ints": 3},'
        ' {"strings": "c", "ints": 2},'
        ' {"strings": "d", "ints": 1}]'
    )

    response = await ac.post("/fetch_data", params={"file_id": 1}, json={"filter_by": ["strings"], "filter_values": ["c"]})
    assert response.status_code == 200
    assert response.json() == '[{"strings": "c", "ints": 2}]'

    response = await ac.delete("delete_file", params={"file_id": 1})
    assert response.status_code == 200
    assert response.json()["message"] == "File deleted successfully."
    assert not os.path.exists(file_path)
