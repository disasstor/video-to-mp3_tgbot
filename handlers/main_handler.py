import asyncio
from urllib.request import urlopen
from PIL import Image
from aiogram import types, Dispatcher
from aiogram.types import InputFile, PhotoSize
from create_bot import bot
from keyboards.generator_kb import get_keyboard
from utils.get_video import get_video, get_media_url, get_media_url_from_playlist
from utils.pillow import get_thumbnail

regex = '(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?'


async def call_playlist(callback_query: types.CallbackQuery):
    await callback_query.answer()
    id_playlist = callback_query.data.split(' ')[1]
    bitrate = callback_query.data.split(' ')[2]
    message_id = callback_query.data.split(' ')[3]
    data_list = get_media_url_from_playlist(id_playlist, bitrate)
    title_playlist = data_list[0]
    title_all = ''
    for i in range(1, len(data_list)):
        title_all += f'{data_list[i]["title"]}\n'
    await callback_query.message.edit_caption(f'<b>{title_playlist}</b>\n\n'
                                              f'{title_all}\n'
                                              f'Bitrate: {bitrate}kbps\n'
                                              f'Download will start in a few minutes...',
                                              parse_mode='HTML')
    for i in range(1, len(data_list)):
        data = data_list[i]
        title = data['title']
        thumbnail = data['thumbnail']
        url = data['url']
        filesize = data['filesize']
        filename = data['filename']
        file = InputFile.from_url(filename=f"{filename}.mp3", url=url, chunk_size=filesize)
        thumbnail_crop = get_thumbnail(thumbnail)
        await bot.send_audio(
            chat_id=callback_query.from_user.id,
            audio=file,
            title=title,
            thumb=thumbnail_crop
        )
        await asyncio.sleep(1)


async def call_video(callback_query: types.CallbackQuery):
    await callback_query.answer()
    id_video = callback_query.data.split(' ')[1]
    bitrate = callback_query.data.split(' ')[2]
    message_id = callback_query.data.split(' ')[3]
    data = get_media_url(id_video, bitrate)
    title = data['title']
    thumbnail = data['thumbnail']
    url = data['url']
    filesize = data['filesize']
    filename = data['filename']
    await callback_query.message.edit_caption(f'<b>Title: {title}</b>\n\n'
                                              f'Bitrate: {bitrate}kbps\n'
                                              f'Download will start in a few minutes...',
                                              parse_mode='HTML')
    file = InputFile.from_url(filename=f"{filename}.mp3", url=url, chunk_size=filesize)
    thumbnail_crop = get_thumbnail(thumbnail)
    await bot.send_audio(
        chat_id=callback_query.from_user.id,
        audio=file,
        title=title,
        thumb=thumbnail_crop
    )


async def help_cmd(message: types.Message):
    await bot.send_message(
        message.from_user.id, f'To download the audio, send the bot a link to the YouTube video.'
    )


async def input_url(message: types.Message):
    url = message.text
    message_id = message.message_id
    data_dict = get_video(url)
    if data_dict is None:
        await bot.send_message(message.from_user.id, 'Video is unavailable')
        return
    if data_dict['type'] == 'video':
        title = data_dict['title']
        thumbnail = data_dict['thumbnail']
        id_video = data_dict['id_video']
        data_list = data_dict['data_list']
        keyboard = get_keyboard(id_video, data_list, message_id, 'video')
        thumbnail_crop = get_thumbnail(thumbnail)
        await message.delete()
        await bot.send_photo(
            chat_id=message.from_user.id,
            photo=thumbnail_crop,
            caption=f'<b>{title}</b>\n\n'
                    f'Please select a music quality.',
            reply_markup=keyboard,
            parse_mode='HTML')

    if data_dict['type'] == 'playlist':
        title = data_dict['title']
        thumbnail = data_dict['thumbnail']
        id_playlist = data_dict['id_playlist']
        data_list = data_dict['data_list']
        count_videos = data_dict['count_videos']
        keyboard = get_keyboard(id_playlist, data_list, message_id, 'playlist')
        thumbnail_crop = get_thumbnail(thumbnail)
        await message.delete()
        await bot.send_photo(
            chat_id=message.from_user.id,
            photo=thumbnail_crop,
            caption=f'<b>{title}</b>\n\n'
                    f'Found {count_videos} videos.\n'
                    f'Please select a music quality.',
            reply_markup=keyboard,
            parse_mode='HTML')


def register_handlers_main(dp: Dispatcher):
    dp.register_message_handler(help_cmd, commands=['start', 'help', 'info', 'старт', 'помощь', 'инфо'])
    dp.register_callback_query_handler(call_video, lambda x: x.data.startswith('video'))
    dp.register_callback_query_handler(call_playlist, lambda x: x.data.startswith('playlist'))
    dp.register_message_handler(input_url, regexp=regex)
