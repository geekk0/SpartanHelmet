import telebot

# Create bot
bot = telebot.TeleBot(token='5431890164:AAHpkETG6FtVQc2FgKZXmdbMtuadvzvuA6E')

# Send message
# bot.send_message(123456798, 'Hi! I\'m a Bot!')


def send_telegram_order_notification(text):
    bot.send_message(1019904124, text)
