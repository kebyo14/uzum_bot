import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))


bot = telebot.TeleBot(TOKEN)

# Сохраняем соответствие между сообщением и пользователем
user_messages = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋 Привет! Напиши своё сообщение, и мы скоро ответим.")

@bot.message_handler(func=lambda message: True)
def forward_to_admin(message):
    if message.chat.id != ADMIN_ID:
        # Сохраняем ID пользователя по ID сообщения
        user_messages[message.message_id] = message.chat.id

        # Пересылаем админу с инфой
        forward_text = f"📩 Новое сообщение от @{message.from_user.username or 'без username'} (ID: {message.chat.id}):\n\n{message.text}"
        sent = bot.send_message(ADMIN_ID, forward_text)
        
        # Запоминаем связь между сообщениями
        user_messages[sent.message_id] = message.chat.id

        bot.send_message(message.chat.id, "✅ Ваше сообщение отправлено. Ожидайте ответа.")
    else:
        # Админ отвечает — проверим, ответ ли это на сообщение
        if message.reply_to_message and message.reply_to_message.message_id in user_messages:
            user_id = user_messages[message.reply_to_message.message_id]
            bot.send_message(user_id, f"💬 Ответ от поддержки:\n\n{message.text}")
        else:
            bot.send_message(ADMIN_ID, "⚠️ Чтобы ответить пользователю, используйте функцию ответа (Reply) на его сообщение.")

if __name__ == '__main__':
    print("🤖 Support bot is running...")
    bot.infinity_polling()
