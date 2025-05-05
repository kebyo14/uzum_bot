import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Sample product database (you can later connect this to your Django backend or API)
products = {
    "iphone": "📱 iPhone 14 - $999\nBuy now: https://uzum.uz/product/iphone-14",
    "macbook": "💻 MacBook Pro - $1999\nBuy now: https://uzum.uz/product/macbook-pro",
    "headphones": "🎧 Sony WH-1000XM5 - $299\nBuy now: https://uzum.uz/product/sony-headphones"
}

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(
        message.chat.id,
        "👋 Welcome to Uzum Market Assistant!\nType a product name like 'iPhone' or 'MacBook' to get started."
    )

@bot.message_handler(func=lambda message: True)
def product_lookup(message):
    query = message.text.lower()
    response = products.get(query)

    if response:
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(
            message.chat.id,
            "❌ Sorry, I couldn't find that product.\nTry searching for 'iPhone', 'MacBook', or 'Headphones'."
        )

if __name__ == "__main__":
    print("🤖 Uzum Market Bot is running...")
    bot.infinity_polling()
