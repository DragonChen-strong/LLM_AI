from fastapi import APIRouter, HTTPException
from models.weather_llm import call_ollama_with_weather

weather_router = APIRouter()


@weather_router.post("/weather")
async def weather_handler(input: str):
    """
    天气查询接口，通过自然语言获取天气信息。
    """
    if not input or not input.strip():
        raise HTTPException(status_code=400, detail="请提供有效的输入参数，例如：'北京的天气怎么样'")

    try:
        # 调用 LLM 模型逻辑
        result = call_ollama_with_weather(input)

        # 判断结果类型
        if isinstance(result, dict) and "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        if not isinstance(result, str):
            raise HTTPException(status_code=500, detail="模型返回了未知的数据格式")



        if not result:
            raise HTTPException(status_code=500, detail="模型返回的数据中缺少 weather_report 字段")

        return {"report": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理天气查询时发生错误：{str(e)}")
