from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 定义生成功能的目标服务器地址
GENERATE_TARGET_URL = "http://192.168.110.175:11434/api/generate"
# 定义聊天功能的目标服务器地址
CHAT_TARGET_URL = "http://192.168.110.175:11434/api/chat"
#定义创建模型
create_TARGET_URL = "http://192.168.110.175:11434/api/create"
#列出本地模型
tags_TARGET_URL = "http://192.168.110.175:11434/api/tags"
#展示模型信息
show_TARGET_URL = "http://192.168.110.175:11434/api/show"
#复制模型
copy_TARGET_URL = "http://192.168.110.175:11434/api/copy"
#删除模型
delete_TARGET_URL = "http://192.168.110.175:11434/api/delete"
#列出正在运行的模型
ps_TARGET_URL = "http://192.168.110.175:11434/api/ps"
#生成嵌入
embed_TARGET_URL = " http://192.168.110.175:11434/api/embed"


@app.route("/my_generate", methods=["POST"])
def my_generate():
    client_data = request.get_json()
    if not client_data:
        return jsonify({"return_code": "5004", "return_info": "请求参数为空"}), 400

    try:
        response = requests.post(GENERATE_TARGET_URL, json=client_data)
        response.raise_for_status()
        response_data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"return_code": "5005", "return_info": "目标服务器连接失败", "error": str(e)}), 502

    return jsonify({"return_code": "200", "return_info": "请求成功", "data": response_data})

@app.route("/my_chat", methods=["POST"])
def my_chat():
    client_data = request.get_json()
    if not client_data:
        return jsonify({"return_code": "5004", "return_info": "请求参数为空"}), 400

    try:
        response = requests.post(CHAT_TARGET_URL, json=client_data)
        response.raise_for_status()
        response_data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"return_code": "5005", "return_info": "目标服务器连接失败", "error": str(e)}), 502

    return jsonify({"return_code": "200", "return_info": "请求成功", "data": response_data})




@app.route("/my_create", methods=["POST"])
def my_create():
    client_data = request.get_json()
    if not client_data:
        return jsonify({"return_code": "5004", "return_info": "请求参数为空"}), 400

    try:
         requests.post(create_TARGET_URL, json=client_data)
    except requests.exceptions.RequestException as e:
        return jsonify({"return_code": "5005", "return_info": "目标服务器连接失败", "error": str(e)}), 502

    return jsonify({"return_code": "200", "return_info": "请求成功"})


@app.route("/my_tags", methods=["GET"])
def my_tags():

    try:
        response = requests.get(tags_TARGET_URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"return_code": "5005", "return_info": "目标服务器连接失败", "error": str(e)}), 502

    return jsonify({"return_code": "200", "return_info": "请求成功"})



@app.route("/my_show", methods=["POST"])
def my_show():
    client_data = request.get_json()
    if not client_data:
        return jsonify({"return_code": "5004", "return_info": "请求参数为空"}), 400

    try:
        response = requests.post(show_TARGET_URL, json=client_data)
        response.raise_for_status()
        response_data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"return_code": "5005", "return_info": "目标服务器连接失败", "error": str(e)}), 502

    return jsonify({"return_code": "200", "return_info": "请求成功", "data": response_data})


@app.route("/my_delete", methods=["DELETE"])
def my_delete():
    client_data = request.get_json()
    if not client_data:
        return jsonify({"return_code": "5004", "return_info": "请求参数为空"}), 400

    try:
        requests.delete(delete_TARGET_URL, json=client_data)
    except requests.exceptions.RequestException as e:
        return jsonify({"return_code": "5005", "return_info": "目标服务器连接失败", "error": str(e)}), 502

    return jsonify({"return_code": "200", "return_info": "请求成功"})


@app.route("/my_ps", methods=["GET"])
def my_ps():

    try:
        response = requests.get(ps_TARGET_URL)
        response.raise_for_status()
        response_data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"return_code": "5005", "return_info": "目标服务器连接失败", "error": str(e)}), 502

    return jsonify({"return_code": "200", "return_info": "请求成功", "data": response_data})


@app.route("/my_copy", methods=["POST"])
def my_copy():
    client_data = request.get_json()
    if not client_data:
        return jsonify({"return_code": "5004", "return_info": "请求参数为空"}), 400

    try:
         requests.post(copy_TARGET_URL, json=client_data)
    except requests.exceptions.RequestException as e:
        return jsonify({"return_code": "5005", "return_info": "目标服务器连接失败", "error": str(e)}), 502

    return jsonify({"return_code": "200", "return_info": "请求成功"})


@app.route("/my_embed", methods=["POST"])
def my_embed():
    client_data = request.get_json()
    if not client_data:
        return jsonify({"return_code": "5004", "return_info": "请求参数为空"}), 400

    try:
        response = requests.post(embed_TARGET_URL, json=client_data)
        response.raise_for_status()
        response_data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"return_code": "5005", "return_info": "目标服务器连接失败", "error": str(e)}), 502

    return jsonify({"return_code": "200", "return_info": "请求成功", "data": response_data})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5010, debug=True)
