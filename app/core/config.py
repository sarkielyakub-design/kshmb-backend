from dotenv import load_dotenv
import os

load_dotenv()


class Settings:

    # =========================
    # DATABASE
    # =========================

    DATABASE_URL = os.getenv(
        "DATABASE_URL"
    )

    # =========================
    # JWT AUTH
    # =========================

    SECRET_KEY = os.getenv(
        "SECRET_KEY"
    )

    ALGORITHM = os.getenv(
        "ALGORITHM"
    )

    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    # =========================
    # CLOUDINARY
    # =========================

    CLOUDINARY_CLOUD_NAME = os.getenv(
        "CLOUDINARY_CLOUD_NAME"
    )

    CLOUDINARY_API_KEY = os.getenv(
        "CLOUDINARY_API_KEY"
    )

    CLOUDINARY_API_SECRET = os.getenv(
        "CLOUDINARY_API_SECRET"
    )


settings = Settings()