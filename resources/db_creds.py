import os
from dotenv import load_dotenv

load_dotenv()

class MoviesDbCreds:
    HOST = os.getenv('DB_MOVIES_HOST')
    PORT = os.getenv('DB_MOVIES_PORT')
    DATABASE = os.getenv('DB_MOVIES_DATABASE')
    USERNAME = os.getenv('DB_MOVIES_USERNAME')
    PASSWORD = os.getenv('DB_MOVIES_PASSWORD')