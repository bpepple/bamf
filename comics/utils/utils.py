import re
from PIL import Image


def test_image(image_path):
    ''' returns a filepath string if the file is valid and not broken '''

    path = ''

    try:
        img = Image.open(image_path)
        img.verify()
        path = image_path
    except Exception:
        pass

    return path

def parse_CV_HTML(string):
    '''
    Parses a string retrieved from ComicVine and parses out unneccessary HTML.
    This is based on the ComicVine text editor.

    Returns parsed string.
    '''

    # Remove <h2>, <h3>, <h4>, <ul>, <ol>, <table> and <figure> tags
    parsed = re.sub(
        '<(table|figure|h2|h3|h4|ul|ol)[^>]*>[\s\S]*?</(table|figure|h2|h3|h4|ul|ol)>', '', string)

    # Unpack <a> tags first because there could be other tags inside.
    # Unpack <a> tags
    parsed = re.sub('</?a[^>]*>', '', parsed)
    # Unpack <b>, <i>, <u>, <s>, <em>, <blockquote> and <strong> tags
    parsed = re.sub('</?(b|i|u|s|em|blockquote|strong)>', '', parsed)

    return parsed