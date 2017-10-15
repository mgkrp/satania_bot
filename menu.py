from utils import build_menu
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import json

def weather_menu(loc, time):
        button_list = [
            InlineKeyboardButton("Yeah, gimme that sweet wall of text", callback_data=json.dumps({'time':time,'loc':loc}))
        ]
        reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
        return reply_markup
