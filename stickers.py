import os
import zipfile
from PIL import Image

def download_sticker(bot, sticker):
    file_id = sticker.file_id
    file = bot.get_file(file_id)
    file.download()

def archive_stickers(bot, update):
    try:
        sticker_set_name = update.message.sticker.set_name
        sticker_set = bot.get_sticker_set(sticker_set_name)
        sticker_set_title = sticker_set.title
        path = os.getcwd()
        for sticker in sticker_set.stickers:
            download_sticker(bot, sticker)
        zip = zipfile.ZipFile('{}.zip'.format(sticker_set_title), 'w', zipfile.ZIP_DEFLATED)
        for file in os.listdir(path):
            if file.startswith('file'):
                zip.write(file)
                os.remove(file)
        zip.close()
        bot.send_document(chat_id=update.message.chat_id, document=open('{}.zip'.format(sticker_set_title), 'rb'))
        os.remove('{}.zip'.format(sticker_set_title))
    except Exception as e:
        print('archive_sticker ')
        print(e)

def add_sticker(bot, update, name):
    try:
        download_sticker(bot, update.message.sticker)
        path = os.getcwd()
        for file in os.listdir(path):
            if file.startswith('file'):
                im = Image.open(file).convert('RGB')
                im.save('sticker.png')
                bot.addStickerToSet(name=name, png_sticker='sticker.png', emojis=update.message.sticker.emoji)
                os.remove(file)
                os.remove('sticker.png')
    except Exception as e:
        print('add_sticker ')
        print(e)

