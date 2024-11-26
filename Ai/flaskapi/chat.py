from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 定义发送请求的目标服务器地址
TARGET_URL = "http://192.168.110.175:11434/api/chat"


@app.route("/my_chat", methods=["POST"])
def my_custom_endpoint():
    # 从请求中获取客户端传入的JSON数据
    client_data = request.get_json()

    # 检查传入的数据是否为空
    if not client_data:
        return jsonify({
            "return_code": "5004",
            "return_info": "请求参数为空"
        }), 400  # 返回HTTP 400状态码，表示客户端错误

    # 发送POST请求到目标服务器并获取响应
    try:
        # 将客户端传入的JSON数据直接转发给目标服务器
        response = requests.post(TARGET_URL, json=client_data)
        response.raise_for_status()  # 检查请求是否成功（状态码200范围内）
        response_data = response.json()  # 获取响应中的JSON数据
    except requests.exceptions.RequestException as e:
        # 处理请求异常情况
        return jsonify({
            "return_code": "5005",
            "return_info": "目标服务器连接失败",
            "error": str(e)
        }), 502  # 返回HTTP 502状态码，表示网关错误

    # 返回目标服务器的响应数据
    return jsonify({
        "return_code": "200",
        "return_info": "请求成功",
        "data": response_data
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5010, debug = 'True')
