# app/main.py
from fastapi import FastAPI
from app.api.endpoints import generate, chat  # 导入路由模块

app = FastAPI()

# 注册各个路由模块
app.include_router(generate.router)
app.include_router(chat.router)
