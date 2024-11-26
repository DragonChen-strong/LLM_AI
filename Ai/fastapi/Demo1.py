import json
from flask import Flask, request, jsonify

app = Flask(__name__)


# 模拟天气API
def get_current_weather(format, location):
    print(f"Calling get_current_weather with format={format}, location={location}")
    if location == "Paris, France":
        return {
            "temperature": 15,
            "condition": "partly cloudy"
        }
    else:
        return {
            "temperature": None,
            "condition": "Unknown location"
        }


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    model = data.get('model')
    messages = data.get('messages')
    tool_calls = data.get('message', {}).get('tool_calls', [])

    response_content = ""
    tool_call_results = []

    for tool_call in tool_calls:
        function_name = tool_call['function']['name']
        arguments = tool_call['function']['arguments']

        if function_name == "get_current_weather":
            result = get_current_weather(arguments['format'], arguments['location'])
            tool_call_results.append({
                "function": {
                    "name": function_name,
                    "arguments": arguments,
                    "result": result
                }
            })
            if result['temperature'] is not None:
                response_content = f"The current weather in {arguments['location']} is {result['temperature']} degrees {arguments['format']} and {result['condition']}."
            else:
                response_content = f"Could not fetch weather information for {arguments['location']}."

    response = {
        "model": model,
        "created_at": data.get('created_at'),
        "message": {
            "role": "assistant",
            "content": response_content,
            "tool_calls": tool_call_results
        },
        "done_reason": "stop",
        "done": True,
        "total_duration": 285590156,
        "load_duration": 70088069,
        "prompt_eval_count": 214,
        "prompt_eval_duration": 20733000,
        "eval_count": 27,
        "eval_duration": 152052000
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11434)