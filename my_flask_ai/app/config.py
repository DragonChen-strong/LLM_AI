# app/config.py
import os
from dotenv import load_dotenv


class Config:
    GENERATE_TARGET_URL = os.getenv("GENERATE_TARGET_URL")
    CHAT_TARGET_URL = os.getenv("CHAT_TARGET_URL")
    CREATE_TARGET_URL = os.getenv("CREATE_TARGET_URL")
    TAGS_TARGET_URL = os.getenv("TAGS_TARGET_URL")
    SHOW_TARGET_URL = os.getenv("SHOW_TARGET_URL")
    COPY_TARGET_URL = os.getenv("COPY_TARGET_URL")
    DELETE_TARGET_URL = os.getenv("DELETE_TARGET_URL")
    PS_TARGET_URL = os.getenv("PS_TARGET_URL")
    EMBED_TARGET_URL = os.getenv("EMBED_TARGET_URL")
