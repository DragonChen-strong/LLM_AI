import uvicorn
from fastapi import FastAPI
from api.weather_router import weather_router   # 导入天气查询的路由模块
from api.hello_router import hello_router
from api.flight_router import flight_router
from api.story_router import story_router


# 创建 FastAPI 应用实例
app = FastAPI()

# 注册天气路由
app.include_router(weather_router)
app.include_router(hello_router)
app.include_router(flight_router)
app.include_router(story_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7502, reload=True)
