import pytube
from pytube import YouTube, Playlist
from pytube.exceptions import RegexMatchError, VideoUnavailable
from pytube.extract import video_id, playlist_id


def get_video(url):
    data_video = get_type(url)
    id_video = data_video[0]
    type_video = data_video[1]
    if type_video == 'video':
        data_dict = get_data(id_video)
        return data_dict
    elif type_video == 'playlist':
        data_dict = get_data_from_playlist(id_video)
        return data_dict


def get_type(url):
    try:
        id_video = video_id(url)
        type_video = 'video'
    except RegexMatchError:
        try:
            id_video = playlist_id(url)
            type_video = 'playlist'
        except RegexMatchError:
            id_video = None
            type_video = None
    return id_video, type_video


def get_data(id_video):
    try:
        url = f'https://youtu.be/{id_video}'
        yt = YouTube(url)
        title = yt.title
        stream = yt.streams
        thumbnail = yt.thumbnail_url
        stream = stream.filter(only_audio=True)
        title = pytube.streams.safe_filename(title, 200)
        bitrate = []
        filesize = []
        for video in stream:
            abr = video.abr
            abr = int(abr.replace('kbps', ''))
            bitrate.append(abr)
            size = video.filesize
            filesize.append(size)
        bitrate.sort()
        filesize.sort()
        data_list = [bitrate, filesize]
        data_list = list(map(list, zip(*data_list)))  # transpose
        data_dict = {
            'type': 'video',
            'id_video': id_video,
            'title': title,
            'thumbnail': thumbnail,
            'data_list': data_list
        }
        return data_dict
    except VideoUnavailable:
        return None


def get_media_url(id_video, bitrate):
    try:
        url = f'https://youtu.be/{id_video}'
        yt = YouTube(url)
        stream = yt.streams
        stream = stream.filter(only_audio=True, abr=f'{bitrate}kbps')
        title = stream[0].title
        filename = pytube.streams.safe_filename(stream[0].title, 200)
        data = {
            'url': stream[0].url,
            'title': title,
            'filename': filename,
            'thumbnail': yt.thumbnail_url,
            'filesize': stream[0].filesize
        }
        return data
    except VideoUnavailable:
        return None


def get_data_from_playlist(id_playlist):
    try:
        url = f'https://www.youtube.com/playlist?list={id_playlist}'
        playlist = Playlist(url)
        title = playlist.title
        data_dict = get_data(playlist.video_urls[0])
        count_videos = len(playlist.video_urls)
        data_dict.update({'type': 'playlist'})
        data_dict['id_playlist'] = id_playlist
        data_dict['title_playlist'] = title
        data_dict['count_videos'] = count_videos
        del data_dict['id_video']
        return data_dict
    except VideoUnavailable:
        return None


def get_media_url_from_playlist(id_playlist, bitrate):
    try:
        url = f'https://www.youtube.com/playlist?list={id_playlist}'
        playlist = Playlist(url)
        title_playlist = playlist.title
        url_list = playlist.video_urls
        data_list = [title_playlist]
        for url in url_list:
            id_video = video_id(url)
            data_list.append(get_media_url(id_video, bitrate))

        return data_list
    except VideoUnavailable:
        return None