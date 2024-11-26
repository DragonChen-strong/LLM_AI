# app/views.py
from flask import Blueprint, request, jsonify, current_app
import requests


bp = Blueprint('views', __name__)

# 生成资源
@bp.route("/my_generate", methods=["POST"])
def my_generate():
    client_data = request.get_json()
    if not client_data:
        return jsonify({"return_code": "5004", "return_info": "请求参数为空"}), 400

    try:
        response = requests.post(current_app.config["GENERATE_TARGET_URL"], json=client_data)
        response.raise_for_status()
        response_data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"return_code": "5005", "return_info": "目标服务器连接失败", "error": str(e)}), 502

    return jsonify({"return_code": "200", "return_info": "请求成功", "data": response_data})

# 聊天功能
@bp.route("/my_chat", methods=["POST"])
def my_chat():
    client_data = request.get_json()
    if not client_data:
        return jsonify({"return_code": "5004", "return_info": "请求参数为空"}), 400

    try:
        response = requests.post(current_app.config["CHAT_TARGET_URL"], json=client_data)
        response.raise_for_status()
        response_data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"return_code": "5005", "return_info": "目标服务器连接失败", "error": str(e)}), 502

    return jsonify({"return_code": "200", "return_info": "请求成功", "data": response_data})

# 创建模型
@bp.route("/my_create", methods=["POST"])
def my_create():
    client_data = request.get_json()
    if not client_data:
        return jsonify({"return_code": "5004", "return_info": "请求参数为空"}), 400

    try:
        requests.post(current_app.config["CREATE_TARGET_URL"], json=client_data)
    except requests.exceptions.RequestException as e:
        return jsonify({"return_code": "5005", "return_info": "目标服务器连接失败", "error": str(e)}), 502

    return jsonify({"return_code": "200", "return_info": "请求成功"})

# 列出本地模型标签
@bp.route("/my_tags", methods=["GET"])
def my_tags():
    try:
        response = requests.get(current_app.config["TAGS_TARGET_URL"])
        response.raise_for_status()
        response_data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"return_code": "5005", "return_info": "目标服务器连接失败", "error": str(e)}), 502

    return jsonify({"return_code": "200", "return_info": "请求成功", "data": response_data})

# 展示模型信息
@bp.route("/my_show", methods=["POST"])
def my_show():
    client_data = request.get_json()
    if not client_data:
        return jsonify({"return_code": "5004", "return_info": "请求参数为空"}), 400

    try:
        response = requests.post(current_app.config["SHOW_TARGET_URL"], json=client_data)
        response.raise_for_status()
        response_data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"return_code": "5005", "return_info": "目标服务器连接失败", "error": str(e)}), 502

    return jsonify({"return_code": "200", "return_info": "请求成功", "data": response_data})

# 删除模型
@bp.route("/my_delete", methods=["DELETE"])
def my_delete():
    client_data = request.get_json()
    if not client_data:
        return jsonify({"return_code": "5004", "return_info": "请求参数为空"}), 400

    try:
        requests.delete(current_app.config["DELETE_TARGET_URL"], json=client_data)
    except requests.exceptions.RequestException as e:
        return jsonify({"return_code": "5005", "return_info": "目标服务器连接失败", "error": str(e)}), 502

    return jsonify({"return_code": "200", "return_info": "请求成功"})

# 列出正在运行的模型
@bp.route("/my_ps", methods=["GET"])
def my_ps():
    try:
        response = requests.get(current_app.config["PS_TARGET_URL"])
        response.raise_for_status()
        response_data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"return_code": "5005", "return_info": "目标服务器连接失败", "error": str(e)}), 502

    return jsonify({"return_code": "200", "return_info": "请求成功", "data": response_data})

# 复制模型
@bp.route("/my_copy", methods=["POST"])
def my_copy():
    client_data = request.get_json()
    if not client_data:
        return jsonify({"return_code": "5004", "return_info": "请求参数为空"}), 400

    try:
        requests.post(current_app.config["COPY_TARGET_URL"], json=client_data)
    except requests.exceptions.RequestException as e:
        return jsonify({"return_code": "5005", "return_info": "目标服务器连接失败", "error": str(e)}), 502

    return jsonify({"return_code": "200", "return_info": "请求成功"})

# 生成嵌入
@bp.route("/my_embed", methods=["POST"])
def my_embed():
    client_data = request.get_json()
    if not client_data:
        return jsonify({"return_code": "5004", "return_info": "请求参数为空"}), 400

    try:
        response = requests.post(current_app.config["EMBED_TARGET_URL"], json=client_data)
        response.raise_for_status()
        response_data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"return_code": "5005", "return_info": "目标服务器连接失败", "error": str(e)}), 502

    return jsonify({"return_code": "200", "return_info": "请求成功", "data": response_data})
