import requests

TELEGRAM_BOT_TOKEN = '8187229531:AAFlGG2TcUgHiNDkqDPOaDtlZJCj2wGXBxs'
CHAT_ID = '5563104704'

def send_telegram_message(message, bot_token, user_id):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        "chat_id": user_id,
        "text": message,
        "parse_mode": "Markdown",
    }
    response = requests.post(url, json=payload)
    return response.json()