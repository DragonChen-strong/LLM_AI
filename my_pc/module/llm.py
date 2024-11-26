import os

import requests
import txt2docx
# 调用 Ollama 模型，返回生成的内容

API_URL="http://192.168.110.175:11434/api/generate"
def call_ollama_model(question):


    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 123"  # 如果需要 `Bearer ` 前缀
    }


    data = {
        "model":"llama3.2:latest",
        "prompt": question,
        "stream": False
    }

    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result.get("response", "模型未返回内容")
    else:
        raise Exception(f"调用 Ollama 模型失败，状态码: {response.status_code}")



# 根据用户选择的文件类型生成对应的文档
def generate_document_from_model(question, file_type="pdf", filename="document"):
    try:
        content = call_ollama_model(question)

        # 根据用户选择的文件类型生成对应的文档
        txt2docx.generate_docx(content, filename=filename)
        print("生成成功")

    except Exception as e:
        print(f"模型调用出错: {e}")
        return "模型调用出错"


# generate_document_from_model("如何优化机器学习模型中的过拟合问题",filename="如何优化机器学习模型中的过拟合问题")



