import json
import requests

LM_STDIO_API_URL = 'http://192.168.91.1:1234/v1/chat/completions'
LM_STDIO_API_KEY = 'lm-studio'

def handler(req, res):
    # 从请求中获取用户输入
    user_input = req.json.get('message')
    
    if not user_input:
        return res.json({"error": "Message is required."}, status=400)
    
    # 设置请求头
    headers = {
        'Authorization': f'Bearer {LM_STDIO_API_KEY}',
        'Content-Type': 'application/json'
    }

    # 设置请求体
    payload = {
        "model": "llama-3.2-3b-instruct",  # 选择合适的模型
        "messages": [{"role": "user", "content": user_input}]
    }

    # 调用 LM stdio API
    response = requests.post(LM_STDIO_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        bot_reply = data.get('choices', [{}])[0].get('message', {}).get('content', 'No response from LM stdio.')
        return res.json({'reply': bot_reply})
    else:
        return res.json({'error': 'Failed to get response from LM stdio'}, status=500)
