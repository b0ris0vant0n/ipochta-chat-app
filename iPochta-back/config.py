from dotenv import load_dotenv
import os

load_dotenv()

# DB Data
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

# Secret
SECRET = os.environ.get("SECRET")

# Redis
BROKER_URL = os.environ.get("BROKER_URL")
RESULT_BACKEND = os.environ.get("RESULT_BACKEND")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
