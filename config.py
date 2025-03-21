import os

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey123")
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///database.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt_secret_key")
SESSION_TIMEOUT = 120  # 2 minutes timeout

