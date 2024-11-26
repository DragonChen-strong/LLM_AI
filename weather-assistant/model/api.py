from flask import Flask, jsonify, request
from model.llm import call_ollama_with_weather

app = Flask(__name__)

@app.route("/weather", methods=["GET"])
def weather_handler():
    """
    获取天气描述的 API。
    用户通过自然语言输入获取天气信息，无需显式传递城市和省份。
    """
    # 获取用户输入
    user_input = request.args.get("input")  # 必须提供自然语言输入

    # 检查输入
    if not user_input:
        return jsonify({"error": "请提供有效的输入参数，例如：input='北京的天气怎么样'"}), 400

    # 调用大模型方法
    result = call_ollama_with_weather(user_input)

    # 检查结果
    if isinstance(result, dict) and "error" in result:
        return jsonify({"error": result["error"]}), 400

    return jsonify({"report": result})


