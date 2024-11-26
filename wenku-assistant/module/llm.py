import os

import requests
import txt2docx
import txt2pdf
import txt2excel
# 调用 Ollama 模型，返回生成的内容
def call_ollama_model(question):


    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 123"  # 如果需要 `Bearer ` 前缀
    }


    data = {
        "model":os.getenv("MODEL_NAME"),
        "prompt": question,
        "stream": False
    }

    response = requests.post(os.getenv("API_URL"), headers=headers, json=data)
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
        if file_type == "docx":
            txt2docx.generate_docx(content, filename=filename)
        elif file_type == "pdf":
            txt2pdf.generate_pdf_from_text(content, filename=filename)
        elif file_type == "excel":
            txt2excel.generate_excel(content, filename=filename)
        else:
            print(f"不支持的文件类型：{file_type}")


    except Exception as e:
        print(f"模型调用出错: {e}")
        return "模型调用出错"



