from ollama import Client

# # 创建 Ollama 客户端
# client = Client(host='http://localhost:11434')
#
# try:
#     # 发送消息并获取响应
#     response = client.chat(
#         model='qwen2:1.5b',  # 确认使用正确的模型名称
#         messages=[
#             {
#                 'role': 'user',
#                 'content': 'Why is the sky blue?',
#             },
#         ]
#     )
#
#     # 打印响应内容
#     print(response['message']['content'])
# except Exception as e:
#     print(f"Error: {e}")

# import ollama
#
# host = "127.0.0.1"
# port = "11434"
# client = ollama.Client(host=f"http://{host}:{port}")
# res = client.chat(model="qwen2:1.5b", messages=[{"role": "user", "content": "你是谁"}], options={"temperature": 0})
#
# print(res)


# import ollama
#
# host = "127.0.0.1"
# port = "11434"
# client = ollama.Client(host=f"http://{host}:{port}")
#
# try:
#     res = client.chat(
#         model="qwen2:1.5b",
#         messages=[{"role": "user", "content": "你是谁"}],
#         options={"temperature": 0}
#     )
#     print(res)
# except Exception as e:
#     print(f"Error: {e}")
#     if hasattr(e, 'response'):
#         print(f"Response: {e.response.text}")


import ollama
# 创建客户端
host = "127.0.0.1"
port = "11434"
client = ollama.Client(host=f"http://{host}:{port}")
try:
    # 调用 chat 方法
    res = client.chat(
        model="qwen2:1.5b",
        messages=[{"role": "user", "content": "你是谁"}],
        options={"temperature": 0}
    )
    print("Response:", res)
except Exception as e:
    print(f"Error: {e}")


