import os
from dotenv import load_dotenv

load_dotenv()

class PostgresCreds:
    HOST = os.getenv('DB_HOST')
    PORT = os.getenv('DB_PORT')
    DATABASE = os.getenv('DB_DATABASE')
    USERNAME = os.getenv('DB_USERNAME')
    PASSWORD = os.getenv('DB_PASSWORD')