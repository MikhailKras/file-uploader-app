import os

from dotenv import load_dotenv

load_dotenv(override=False)

APP_NAME = os.getenv('APP_NAME')

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

DB_HOST_TEST = os.getenv("DB_HOST_TEST")
DB_PORT_TEST = os.getenv("DB_PORT_TEST")
DB_NAME_TEST = os.getenv("DB_NAME_TEST")
DB_USER_TEST = os.getenv("DB_USER_TEST")
DB_PASS_TEST = os.getenv("DB_PASS_TEST")
