# mmm.py

import requests
from flask import Flask, render_template, request, jsonify

# LM stdio API 配置（假设有此 API）
LM_STDIO_API_URL = 'http://192.168.91.1:1234/v1/chat/completions'  # 用于聊天的 API URL
LM_STDIO_API_KEY = 'lm-studio'                    # 替换为实际的 API 密钥

app = Flask(__name__)

# 调用 LM stdio 模型的函数
def get_bot_response(user_input):
    headers = {
        'Authorization': f'Bearer {LM_STDIO_API_KEY}',
        'Content-Type': 'application/json'
    }

    # 创建请求体
    payload = {
        "model": "llama-3.2-3b-instruct",  # 假设你使用的是 GPT 模型，根据你的实际模型名称调整
        "messages": [{"role": "user", "content": user_input}]
    }

    # 发送 POST 请求到 LM stdio API
    response = requests.post(LM_STDIO_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        # 假设 API 返回 JSON 格式的响应
        data = response.json()
        return data.get('choices', [{}])[0].get('message', {}).get('content', 'No response from LM stdio.')
    else:
        # 如果请求失败，返回错误信息
        return f"Error: {response.status_code}, {response.text}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message']
    bot_reply = get_bot_response(user_input)
    return jsonify({'reply': bot_reply})

if __name__ == '__main__':
    app.run(debug=True)
