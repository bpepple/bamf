import os
import uuid

from PIL import Image
from django.conf import settings

THUMBNAIL_WIDTH = 200
THUMBNAIL_HEiGHT = 305

NORMAL_WIDTH = 320
NORMAL_HEIGHT = 487


def resize_images(path, folder, thumb):
    if path:
        # Split width and height
        if not thumb:
            crop_width = NORMAL_WIDTH
            crop_height = NORMAL_HEIGHT
        else:
            crop_width = THUMBNAIL_WIDTH
            crop_height = THUMBNAIL_HEiGHT

        old_filename = os.path.basename(str(path))
        (shortname, ext) = os.path.splitext(old_filename)
        # 18 characters should be more than enough.
        new_filename = str(uuid.uuid4())
        if not thumb:
            cache_path = 'images/' + folder + '/normal/' + new_filename + ext
        else:
            cache_path = 'images/' + folder + '/thumbnails/' + new_filename + ext

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


def truncate_description(desc_txt):
    # TODO: Truncate to last sentence instead of character.
    if len(desc_txt) > 500:
        desc = desc_txt[:496] + '...'
    else:
        desc = desc_txt

    return desc


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
