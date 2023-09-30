from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ARRAY

from src.database import metadata

file_info = Table(
    'file_info',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('file_name', String, nullable=False),
    Column('uploaded_time', TIMESTAMP, default=datetime.utcnow),
    Column('column_names', ARRAY(String))
)
