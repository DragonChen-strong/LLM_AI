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
        "weather_type": os.getenv("WEATHER_API_TYPE", "observe|forecast_24h"),
    }

    #ollama API配置
    LLM_URL = os.getenv("LLM_URL", "http://192.168.110.175:11434/api/generate")
    LLM_MODEL = os.getenv("LLM_MODEL", "codegemma:7b")
    API_PORT = int(os.getenv("API_PORT", 5000))

config = Config()
