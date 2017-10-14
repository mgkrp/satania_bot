from utils import build_menu
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def weather_menu():
        button_list = [
            [InlineKeyboardButton("Yeah, gimme that sweet wall of text", callback_data=...),
            InlineKeyboardButton("Nah, I'm fine", callback_data=...)]
        ]
        reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
        return reply_markup
