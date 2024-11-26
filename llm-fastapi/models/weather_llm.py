from langchain_experimental.llms.ollama_functions import OllamaFunctions
from models.weather import get_weather_info
import json
from core.config import config



# 初始化 OllamaFunctions 模型
model = OllamaFunctions(
    model=config.LLM_MODEL,
    base_url=config.LLM_URL,
    format="json"  # 输出格式设置为 JSON
)

# 定义封装后的天气查询函数
def get_weather(user_input):
    weather_data = get_weather_info(user_input)
    return weather_data


# 工具映射列表
function_map = {
    'get_weather': get_weather
}


# 定义工具
tools = [
    {
        "name": "get_weather",
        "description": "获取指定地区的天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "user_input": {
                    "type": "string",
                    "description": "用户输入的查询内容，例如：南京的天气怎么样？"
                }
            },
            "required": ["user_input"]
        }
    }
]


# 绑定工具
llm_with_tool = model.bind_tools(
    tools=tools,
)

def call_ollama_with_weather(user_input):

    message = [
        {"role": "system", "content": """
            你是一个智能天气助手，可以帮助用户回答任何关于天气的问题。
            你将基于提供的天气数据和用户问题生成答案。
               规则：
               1. 如果用户提出天气相关问题（例如“南京的天气怎么样？”），调用工具 `get_weather` 并提供用户输入内容。
               2. 下面问题一定要根据工具返回的数据生成响应，生成一份详细的天气描述，全部都用中文进行描述，要求如下：
                  - 包含当前日期和地点（例如“2024年11月20日，江苏连云港”）。
                  - 描述实时天气情况，包括天气现象、最高温度、最低温度、湿度、降水量、风力、气压等信息。
                  - 提供生活建议（如穿衣、运动、洗车等）。**生活建议多说一点**"""},
    ]

    # 调用模型并获取初始响应
    res = llm_with_tool.invoke(user_input)

    def_name = json.loads(res.json()).get("tool_calls", [])
    if def_name:
        name=def_name[0]['name']
        function_action=function_map.get(name,None)
        if function_action:
           result= function_action(**def_name[0]["args"])
           message.append(
               {
                   "role": "tool",
                   "tool_call_id": def_name[0]["id"],
                   "name": name,
                   "content": str(result)
               }
           )
           res=llm_with_tool.invoke(json.dumps(message))



    return res.content
