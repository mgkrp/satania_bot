from telegram.ext import Updater, Handler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import CallbackQuery, InputTextMessageContent

from weather import get_current_weather, get_additional_info
from stickers import archive_stickers, create_sticker_set, add_sticker

import uuid
import json
import os

updater = Updater(token='447516508:AAF6YtND_qQAGsKu4jTpJFSWfkgk18vEtww')
dispatcher = updater.dispatcher

# settings for bot

settings = {
    'sticker_set': False, # check if sticker should be uploaded to the set
    'current_set': None  # current sticker set
}

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
    try:
        response, icon, location, reply_markup = get_current_weather(location, time)
    except Exception as e:
        print(e)
    response = ''.join(['Weather for ', location, '\n\n', response])
    bot.send_message(chat_id=update.message.chat_id, text=response)
    if reply_markup != None:
        try:
            bot.send_message(chat_id=update.message.chat_id, text="Do you wanna see more?", reply_markup=reply_markup)
        except Exception as e:
            print(e)

def stickers(bot, update):
    if not settings['sticker_set']:
        bot.send_message(chat_id=update.message.chat_id, text="Hold up, I'm getting your stickers nice and ready.")
        sticker_set_title = archive_stickers(bot, update)
    elif settings['current_set'] != None:
        add_sticker(bot, update, settings['current_set'])
    else:
        pass
        # TODO later


def start_sticker_set(bot, update, args):
    set_name = create_sticker_set(bot, update, args)
    settings.current_set = set_name
    settings.sticker_set = True
    print(settings)


def finish_sticker_set(bot, update):
    settings.sticker_set = False
    sticker_set = bot.get_sticker_set(settings['current_set'])
    bot.send_sticker(chat_id=update.message.chat_id, sticker=sticker_set.stickers[0].file_id)
    

def callback_weather(bot, update):
    query = update.callback_query
    data = json.loads(query.data)
    response = get_additional_info(loc=data.loc, time=data.time)
    bot.edit_message_text(text=response,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

def test(bot, update):
    print(update)
   
def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Wakanayo~")

# handlers
start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text, echo)
caps_handler = CommandHandler('caps', caps, pass_args=True)

# weather handlers
weather_handler = CommandHandler('weather', weather, pass_args=True)
callback_weather_handler = CallbackQueryHandler(callback_weather)

# stickers handler
sticker_handler = MessageHandler(Filters.sticker, stickers)
start_set_handler = CommandHandler('stickerstart', start_sticker_set, pass_args=True)
finish_set_handler = CommandHandler('stickerfinish', finish_sticker_set)

# handler for testing stuff
test_handler = CommandHandler('test', test)

# unknown command handler
unknown_handler = MessageHandler(Filters.command, unknown)

# dispatchers
dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(caps_handler)
dispatcher.add_handler(weather_handler)
dispatcher.add_handler(callback_weather_handler)
dispatcher.add_handler(sticker_handler)
dispatcher.add_handler(start_set_handler)
dispatcher.add_handler(finish_set_handler)
dispatcher.add_handler(test_handler)

# unknow dispatcher
dispatcher.add_handler(unknown_handler)

updater.start_polling()
