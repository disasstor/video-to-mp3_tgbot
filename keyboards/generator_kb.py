from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_keyboard(id_video, data_list, message_id, type):
    # Генерация клавиатуры
    buttons = []
    if type == 'video':
        for data in data_list:
            bitrate = int(data[0])
            filesize = data[1]
            filesize = float('%.2f' % (filesize / 1024 / 1024))
            buttons.append(
                InlineKeyboardButton(
                    f'{bitrate}kbps ({filesize}mb)',
                    callback_data=f'{type} {id_video} {bitrate} {message_id}'
                )
            )
    elif type == 'playlist':
        for data in data_list:
            bitrate = data[0]
            buttons.append(
                InlineKeyboardButton(
                    f'{bitrate}kbps',
                    callback_data=f'{type} {id_video} {bitrate} {message_id}'
                )
            )
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard
