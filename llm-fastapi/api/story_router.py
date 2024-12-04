from fastapi import APIRouter, HTTPException
from models.story_split_llm import call_story_to_picture

story_router = APIRouter()


@story_router.post("/story")
async def weather_handler(input: str):
    """
    天气查询接口，通过自然语言获取天气信息。
    """
    if not input or not input.strip():
        raise HTTPException(status_code=400, detail="请提供一段有趣的故事情节")

    try:
        # 调用 LLM 模型逻辑
        result = call_story_to_picture(input)

        # 判断结果类型
        if isinstance(result, dict) and "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])


        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成故事时发生错误：{str(e)}")
