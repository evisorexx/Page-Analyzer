from bs4 import BeautifulSoup


def parser(content):
    html = BeautifulSoup(content, 'html.parser')
    meta = html.find('meta', attrs={'name': 'description'})
    description = None
    if meta:
        description = meta.get('content', None)
    result = {
        'h1': html.h1.get_text() if html.h1 else None,
        'title': html.title.get_text() if html.title else None,
        'description': description
    }
    return result
