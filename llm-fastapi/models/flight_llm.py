from langchain_experimental.llms.ollama_functions import OllamaFunctions
from models.flight import get_flights, cancel_flight_by_details  # 假设你有航班相关的函数
import json
from core.config import config


class AssistantTools:
    def __init__(self):
        # 初始化 OllamaFunctions 模型
        self.model = OllamaFunctions(
            model=config.LLM_MODEL,
            base_url=config.LLM_URL,
            format="json"  # 输出格式设置为 JSON
        )

        # 定义工具
        self.tools = [
            {
                "name": "get_flights",
                "description": """
                        获取用户的航班信息。
                        你需要从用户输入中提取查询条件（如日期、出发城市、到达城市等）。
                         例如：用户可能说“查看2024年12月1日从南京到北京的航班”或“查看从北京到上海的航班”。
                        工具参数：
                        - departure_city: 出发城（可选），例如“南京”。
                        - arrival_city: 到达城市（可选），例如“北京”。
                        - departure_date: 航班日期（可选），例如“2024年12月1日”。
                        如果没有提供日期，则返回最近几天的航班信息。
                    """,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "departure_city": {
                            "type": "string",
                            "description": "出发城市，例如：南京"
                        },
                        "arrival_city": {
                            "type": "string",
                            "description": "到达城市，例如：北京"
                        },
                        "departure_date": {
                            "type": "string",
                            "description": "航班日期，例如：2024年12月1日"
                        }
                    },
                    "required": []
                }
            },
            {
                "name": "cancel_flight",
                "description": """
                        取消用户的航班。
                        你需要从输入中提取航班的信息，日期、出发地、目的地。
                        例如：用户可能说“取消2024年12月1日从南京到上海的航班”。
                        工具参数：
                        - departure_city: 出发城市，例如“南京”。
                        - arrival_city: 到达城市，例如“上海”。
                        - date: 航班日期，例如“2024年12月1日”。
                    """,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "departure_city": {
                            "type": "string",
                            "description": "出发城市，例如：南京"
                        },
                        "arrival_city": {
                            "type": "string",
                            "description": "到达城市，例如：上海"
                        },
                        "departure_date": {
                            "type": "string",
                            "description": "航班日期，例如：2024年12月1日"
                        }
                    },
                    "required": ["departure_city", "arrival_city", "departure_date"]
                }
            }
        ]

        # 工具映射列表
        self.function_map = {
            'get_flights': self.get_flights,
            'cancel_flight': self.cancel_flight
        }

        # 绑定工具到模型
        self.llm_with_tool = self.model.bind_tools(tools=self.tools)


    # 查询航班功能
    def get_flights(self, departure_city=None,arrival_city=None,departure_date=None):
        # 直接调用查询航班的函数，传递模型提取的查询条件
        flight_data = get_flights(departure_city,arrival_city,departure_date)
        return flight_data


    # 取消航班功能
    def cancel_flight(self, departure_city,arrival_city,departure_date):
        # 直接调用取消航班的函数，传递模型提取的航班详细信息
        result = cancel_flight_by_details(departure_city,arrival_city,departure_date)
        return result


    # 实现助手功能，通过调用大模型并自动选择合适的工具
    def call_with_assistant(self, user_input):
        # 初始对话内容，用于设定大模型的角色和规则
        message = [
            {"role": "system", "content": """
                    你是一个智能助手，可以帮助用户回答航班的问题。
                    **你将基于提供的航班数据和用户问题生成答案**。
                    下面问题一定要根据工具返回的数据生成响应，生成一份详细的航班描述，全部都用中文进行描述，要求如下：
                    - 包含当前日期和地点（例如“2024年11月20日，北京到上海）。
                    - 通过解析数据格式，将详细信息结合自己去表达出来
                """}
        ]

        # 调用模型并获取初始响应
        res = self.llm_with_tool.invoke(user_input)

        # 处理模型返回的工具调用请求
        tool_calls = json.loads(res.json()).get("tool_calls", [])
        if tool_calls:
            tool_call = tool_calls[0]
            function_name = tool_call['name']
            function_action = self.function_map.get(function_name)

            if function_action:
                # 获取工具函数的结果
                result = function_action(**tool_call["args"])

                message.append(
                    {
                        "role": "role",
                        "content": str(result)
                    }
                )

                # 再次调用模型，生成完整响应
                try:
                    res = self.llm_with_tool.invoke(json.dumps(message))
                except ValueError as e:
                    # 捕获异常并手动提取 content 或 answer 部分
                    response_text = str(e)
                    start_index = response_text.find('"content":')
                    if start_index != -1:
                        start_index += len('"content":')
                        content_part = response_text[start_index:].strip()
                        try:
                            # 提取 content 部分，去掉前后多余字符
                            content = json.loads(content_part)
                            return content
                        except json.JSONDecodeError:
                            # 如果直接解析失败，可能需要手动去掉多余字符
                            end_index = content_part.rfind('}')
                            if end_index != -1:
                                return content_part[:end_index].strip().strip('"')

                    # 处理 "answer" 字段的情况
                    start_index = response_text.find('"answer":')
                    if start_index != -1:
                        start_index += len('"answer":')
                        answer_part = response_text[start_index:].strip()
                        try:
                            # 提取 answer 部分，去掉前后多余字符
                            answer = json.loads(answer_part)
                            return answer
                        except json.JSONDecodeError:
                            # 如果直接解析失败，手动去除多余字符
                            end_index = answer_part.rfind('}')
                            if end_index != -1:
                                return answer_part[:end_index].strip().strip('"')

                        return response_text

        return res.content


AssistantTools=AssistantTools()
res=AssistantTools.call_with_assistant("2024年12月1日航班信息")
print(res)