from flask import Flask, request, jsonify
from module.llm import generate_document_from_model
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)



@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    question = data.get("question")
    file_type = data.get("file_type", "pdf")
    filename = data.get("filename", "output")

    try:
        generate_document_from_model(question, file_type=file_type, filename=filename)
        return jsonify({"message": "Document generated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("FLASK_RUN_PORT",5011)))

