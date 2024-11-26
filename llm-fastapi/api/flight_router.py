from fastapi import APIRouter, HTTPException
from models.flight_llm import AssistantTools


flight_router = APIRouter()

# 初始化 AssistantTools
assistant_tools = AssistantTools()

@flight_router.post("/flight")
async def weather_handler(input: str):
    """
    天气查询接口，通过自然语言获取天气信息。
    """
    if not input or not input.strip():
        raise HTTPException(status_code=400, detail="请提供有效的输入参数，例如：'查看2024年12月1日从北京飞往上海的航班'")

    try:

        response = assistant_tools.call_with_assistant(input)
        # 调用 LLM 模型逻辑

        # 返回处理后的结果
        return {"status": "success", "result": response}


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理天气查询时发生错误：{str(e)}")
