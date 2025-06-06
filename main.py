import time
import requests
import random

TOKEN = '8107582287:AAE3XkCCqKt1T7TAtaqlp4bw57c2EIYSHJs'  # 👉 вставь свой токен от BotFather
URL = f"https://api.telegram.org/bot{TOKEN}"
WEBAPP_URL = "https://rayytsx.github.io/case.gift/"  # Готовое мини-приложение
last_update_id = 0

prizes = [
    "🔹 Легендарный нож",
    "🔸 Эпический скин",
    "⚪ 500 коинов",
    "🔻 Ничего не выпало...",
    "💠 Сюрприз-кейс",
    "💣 Бонус-кейс на 2 открытия"
]

def get_updates():
    try:
        response = requests.get(f"{URL}/getUpdates?offset={last_update_id + 1}")
        return response.json()
    except Exception as e:
        print(f"Ошибка при получении обновлений: {e}")
        return {}

def send_message(chat_id, text, with_webapp=False):
    try:
        if with_webapp:
            keyboard = {
                "inline_keyboard": [[{
                    "text": "🎁 Открыть кейс",
                    "web_app": {"url": WEBAPP_URL}
                }]]
            }
            data = {
                "chat_id": chat_id,
                "text": text,
                "reply_markup": keyboard
            }
            requests.post(f"{URL}/sendMessage", json=data)
        else:
            requests.get(f"{URL}/sendMessage?chat_id={chat_id}&text={text}")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")

def handle_updates(updates):
    global last_update_id
    for update in updates.get("result", []):
        last_update_id = update["update_id"]
        message = update.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "")

        if not chat_id:
            continue

        if text == "/start":
            send_message(chat_id, "🎮 Добро пожаловать в LuckyCase! Жми кнопку ниже, чтобы открыть кейс:", with_webapp=True)
        elif text == "/open":
            prize = random.choice(prizes)
            send_message(chat_id, f"📦 Ты открыл кейс и получил: {prize}")
        else:
            send_message(chat_id, "❓ Не понял тебя. Напиши /start или /open.")

while True:
    updates = get_updates()
    handle_updates(updates)
    time.sleep(2)
