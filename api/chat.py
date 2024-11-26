import os
import requests
from flask import Flask, request, jsonify

# 初始化 Flask 应用
app = Flask(__name__)

# 获取 LM stdio API 密钥和 URL（可以在环境变量中设置）
# API_KEY = os.getenv("LM_STDIO_API_KEY")  # 使用环境变量存储 API 密钥
API_KEY = "lm-studio"
API_URL = "http://192.168.91.1:1234/v1/chat/completions"  # LM stdio 的 API URL，假设本地部署

# 聊天路由
@app.route("/api/chat", methods=["POST"])
def chat():
    # 从请求中获取用户的消息
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # 请求 LM stdio API 获取响应
    response = requests.post(
        API_URL,
        json={"messages": [{"role": "user", "content": user_message}]},
        headers={"Authorization": f"Bearer {API_KEY}"},
    )

    # 处理 API 响应
    if response.status_code == 200:
        data = response.json()
        bot_reply = data.get("choices")[0].get("message").get("content")
        return jsonify({"reply": bot_reply})
    else:
        return jsonify({"error": "Failed to get response from LM stdio"}), 500


# 在 Vercel 上，Flask 应用会自动调用路由，无需调用 app.run()
