from validators import url
from urllib.parse import urlparse


def normalize_url(url_to_normalize):
    result = urlparse(url_to_normalize)
    return f'{result[0]}://{result[1]}'


def validate_url(url_to_check: str):
    if len(url_to_check) > 255 or not url(url_to_check):
        return False
    else:
        return True
