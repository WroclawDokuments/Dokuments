import os
import telebot
from flask import Flask, request

TOKEN = os.getenv("BOT_TOKEN", "7789778927:AAELqG2MxUw_nQb6kvIsyfMdeRx6fMZCzTc")
ADMIN_ID = int(os.getenv("ADMIN_ID", "457920866"))

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route("/")
def index():
    return "🤖 Бот работает!"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "👋 Привет! Напиши своё сообщение, и мы обязательно свяжемся с тобой.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user = message.from_user
    text = f"📩 Новое сообщение от @{user.username or user.first_name} (ID: {user.id}):\n\n{message.text}"
    bot.send_message(ADMIN_ID, text)
    bot.reply_to(message, "✅ Спасибо! Ваше сообщение отправлено. Мы скоро свяжемся с вами.")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{os.getenv('RENDER_EXTERNAL_URL')}/{TOKEN}")
