import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

class Config:
    FLASK_ENV = os.getenv("FLASK_ENV", "development")

    #天气API配置
    WEATHER_API_URL = os.getenv("WEATHER_API_URL", "https://wis.qq.com/weather/common")
    WEATHER_API_PARAMS = {
        "source": os.getenv("WEATHER_API_SOURCE", "pc"),
        "weather_type": os.getenv("WEATHER_API_TYPE", "observe"),
    }

    #ollama API配置
    LLM_URL = os.getenv("LLM_URL", "http://192.168.110.175:11434/api/generate")
    LLM_MODEL = os.getenv("LLM_MODEL", "codegemma:7b")
    API_PORT = int(os.getenv("API_PORT", 5000))

    # 数据库
    DB_HOST = os.getenv("DB_HOST","192.168.110.175")
    DB_PORT = os.getenv("DB_PORT","3306")
    DB_USER = os.getenv("DB_USER","root")
    DB_PASSWORD =os.getenv("DB_PASSWORD","root@JDkj!123")
    DB_NAME = os.getenv("DB_NAME","jdkj_bean_ai")

config = Config()
