import os
import uuid
import re
from bs4 import BeautifulSoup

from PIL import Image
from django.conf import settings

NORMAL_WIDTH = 320
NORMAL_HEIGHT = 487


def resize_images(path, folder):
    if path:
        # Split width and height
        crop_width = NORMAL_WIDTH
        crop_height = NORMAL_HEIGHT

        old_filename = os.path.basename(str(path))
        (shortname, ext) = os.path.splitext(old_filename)
        # 18 characters should be more than enough.
        new_filename = str(uuid.uuid4())
        cache_path = 'images/' + folder + '/' + new_filename + ext

        new_path = settings.MEDIA_ROOT + '/' + cache_path
        new_url = cache_path

        try:
            img = Image.open(settings.MEDIA_ROOT + '/images/' + old_filename)
            # Check Aspect ratio and resize accordingly
            if crop_width * img.height < crop_height * img.width:
                height_percent = (float(crop_height) / float(img.size[1]))
                width_size = int(float(img.size[0]) * float(height_percent))
                img = img.resize((width_size, crop_height), Image.BICUBIC)
            else:
                width_percent = (float(crop_width) / float(img.size[0]))
                height_size = int(float(img.size[1]) * float(width_percent))
                img = img.resize((crop_width, height_size), Image.BICUBIC)

            cropped = crop_from_center(img, crop_width, crop_height)
            cropped.save(new_path)
        except Exception:
            # Save as blank instead of None for bad images.
            new_url = ''

    return new_url


def crop_from_center(image, width, height):
    img = image
    center_width = img.size[0] / 2
    center_height = img.size[1] / 2
    cropped = img.crop(
        (
            center_width - width / 2,
            center_height - height / 2,
            center_width + width / 2,
            center_height + height / 2
        )
    )

    return cropped


def create_series_sortname(title):
    sort_name = title
    contains_the = sort_name.startswith('The ')
    if contains_the:
        sort_name = sort_name.replace('The ', '')
        sort_name = sort_name + ', The'

    return sort_name


def cleanup_html(string, remove_html_tables):
    if string is None:
        return ""
    # find any tables
    soup = BeautifulSoup(string, 'html.parser')
    tables = soup.findAll('table')

    # remove all newlines first
    string = string.replace("\n", "")

    # put in our own
    string = string.replace("<br>", "\n")
    string = string.replace("</p>", "\n\n")
    string = string.replace("<h4>", "*")
    string = string.replace("</h4>", "*\n")

    # remove the tables
    p = re.compile(r'<table[^<]*?>.*?<\/table>')
    if remove_html_tables:
        string = p.sub('', string)
        string = string.replace("*List of covers and their creators:*", "")
    else:
        string = p.sub('{}', string)

    # now strip all other tags
    p = re.compile(r'<[^<]*?>')
    newstring = p.sub('', string)

    newstring = newstring.replace('&nbsp;', ' ')
    newstring = newstring.replace('&amp;', '&')

    newstring = newstring.strip()

    if not remove_html_tables:
        # now rebuild the tables into text from BSoup
        try:
            table_strings = []
            for table in tables:
                rows = []
                hdrs = []
                col_widths = []
                for hdr in table.findAll('th'):
                    item = hdr.string.strip()
                    hdrs.append(item)
                    col_widths.append(len(item))
                rows.append(hdrs)

                for row in table.findAll('tr'):
                    cols = []
                    col = row.findAll('td')
                    i = 0
                    for c in col:
                        item = c.string.strip()
                        cols.append(item)
                        if len(item) > col_widths[i]:
                            col_widths[i] = len(item)
                        i += 1
                    if len(cols) != 0:
                        rows.append(cols)
                # now we have the data, make it into text
                fmtstr = ""
                for w in col_widths:
                    fmtstr += " {{:{}}}|".format(w + 1)
                width = sum(col_widths) + len(col_widths) * 2
                table_text = ""
                counter = 0
                for row in rows:
                    table_text += fmtstr.format(*row) + "\n"
                    if counter == 0 and len(hdrs) != 0:
                        table_text += "-" * width + "\n"
                    counter += 1

                table_strings.append(table_text)

            newstring = newstring.format(*table_strings)
        except:
            # we caught an error rebuilding the table.
            # just bail and remove the formatting
            print("table parse error")
            newstring.replace("{}", "")

    # Truncate the string if it's still over 500 characters long.
    if len(newstring) > 500:
        newstring = newstring[:499]

    return newstring


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
