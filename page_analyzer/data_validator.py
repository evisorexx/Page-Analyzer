from validators import url


def validate_url(url_to_check: str):
    if len(url_to_check) > 255:
        return False
    return url(url_to_check)
