import os
from datetime import timedelta

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/tasksdb")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key_here")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
