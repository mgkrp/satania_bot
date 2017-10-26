import os
import zipfile

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
        print(e)

def add_sticker(bot, update, name):
    bot.add_sticker_to_set(name=name, png_sticker=update.message.sticker.file_id, emojis=update.message.sticker.emojis)

def create_sticker_set(bot, update, name):
    try:
        bot.createNewStickerSet(user_id=update.message.chat.id, name=name[0]+'_by_satania_bot', title=name)
        return name[0]+'_by_satania_bot'
    except Exception as e:
        print(e)