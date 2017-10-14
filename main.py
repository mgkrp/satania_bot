from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent

from weather import get_current_weather

import uuid


updater = Updater(token='447516508:AAF6YtND_qQAGsKu4jTpJFSWfkgk18vEtww')
dispatcher = updater.dispatcher

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please don't bulli me!")

def echo(bot, update):
    text = update.message.text
    odd = True
    response = ''
    for char in text:
        if (odd):
            response = response + char.upper()
        else:
            response = response + char.lower()
        odd = not(odd)
    bot.send_message(chat_id=update.message.chat_id, text=response)
    bot.send_photo(chat_id=update.message.chat_id, photo='https://memegenerator.net/img/images/250x250/17446874/spongebob-chicken-meme.jpg')

def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)

def weather(bot, update, args):
    if len(args) == 0:
        location = 'spbru'
        time = 'now'
    else:
        location = args[0]
        time = args[1]
    if (time == 'hourly')
    response, icon, location = get_current_weather(location, time)
    response = ''.join(['Weather for ', location, '\n\n', response])
    bot.send_message(chat_id=update.message.chat_id, text=response)

   
def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Wakanayo~")

# handlers
start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text, echo)
caps_handler = CommandHandler('caps', caps, pass_args=True)

weather_handler = CommandHandler('weather', weather, pass_args=True)

# unknown handler
unknown_handler = MessageHandler(Filters.command, unknown)

# dispatchers
dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(caps_handler)
dispatcher.add_handler(weather_handler)

# unknow dispatcher
dispatcher.add_handler(unknown_handler)

updater.start_polling()