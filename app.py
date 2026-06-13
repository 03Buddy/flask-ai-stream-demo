import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, Response, stream_with_context

load_dotenv()
app = Flask(__name__)

# 读取环境变量，密钥不写死在代码
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"

# 基础prompt模板
BASE_PROMPT = "你是简洁高效的AI助手，回答精简有条理，不冗余。用户问题："

# 流式生成器
def generate_answer(user_input):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": BASE_PROMPT},
            {"role": "user", "content": user_input}
        ],
        "stream": True,
        "temperature": 0.7
    }
    response = requests.post(API_URL, json=payload, headers=headers, stream=True)
    # SSE流式逐字返回
    for chunk in response.iter_lines():
        if chunk:
            line = chunk.decode("utf-8")
            if line.startswith("data: "):
                data = line[6:]
                if data == "[DONE]":
                    break
                yield f"data: {data}\n\n"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/stream", methods=["POST"])
def stream():
    user_text = request.form.get("user_input", "")
    return Response(
        stream_with_context(generate_answer(user_text)),
        mimetype="text/event-stream"
    )

if __name__ == "__main__":
    app.run(debug=False)