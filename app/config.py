import os


class Settings():
    db_url = os.getenv("DATABASE_URL")


settings = Settings()
