import ollama

# # 获取模型
# # model = ollama.get_model("qwen2.5:1.5b")
#
# # 对话历史记录
# messages = [
#     {"role": "user", "content": "Hello, how are you?"},
#     {"role": "assistant", "content": "Hi, I'm doing well. How about you?"}
# ]
#
# # 生成回复
# response=ollama.chat(messages=messages, model="qwen2.5:1.5b",stream=True)
#
#
# for chunk in response:
#     if 'messages' in chunk and 'content' in chunk['messages']:
#         print(chunk['messages']['content'])

import ollama

# # 获取模型列表
# model_list = ollama.list()
#
# # 对话历史记录
# messages = [
#     {"role": "user", "content": "Hello, how are you?"},
#     {"role": "assistant", "content": "Hi, I'm doing well. How about you?"}
# ]
#
# # 选择模型
# model_name = "qwen2.5:1.5b"
#
# # 打印模型列表和选择的模型名称
# print(model_list)
# print(f"Selected model: {model_name}")
#
# try:
#     # 生成回复
#     response = ollama.chat(messages=messages, model=model_name, stream=False)
#
#     for chunk in response:
#         print(chunk)  # 打印 chunk 的内容
#         if 'messages' in chunk and 'content' in chunk['messages']:
#             print(chunk['messages']['content'])
# except Exception as e:
#     print(f"An error occurred: {e}")

import ollama

# 获取模型列表
model_list = ollama.list()

# 对话历史记录
messages = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "Hi, I'm doing well. How about you?"}
]

# 选择模型
model_name = "qwen2.5:1.5b"

# 打印模型列表和选择的模型名称
print(model_list)
print(f"Selected model: {model_name}")

try:
    # 生成回复
    response = ollama.chat(messages=messages, model=model_name, stream=False)

    # 打印完整的响应内容
    print(response)

    if 'message' in response and 'content' in response['message']:
        content = response['message']['content']
        if content:
            print(content)
        else:
            print("No content generated.")
    else:
        print("Response structure does not contain expected fields.")
except Exception as e:
    print(f"An error occurred: {e}")