from PIL import Image
from urllib.request import urlopen
from io import BytesIO


def get_thumbnail(url):
    img = Image.open(urlopen(url))
    img = img.crop((0, 60, 640, 420))  # (left, top, right, bottom)
    bio = BytesIO()
    bio.name = 'thumbnail.jpeg'
    img.save(bio, 'JPEG')
    bio.seek(0)
    return bio
