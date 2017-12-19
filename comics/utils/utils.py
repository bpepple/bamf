import os

from PIL import Image
from django.conf import settings


def resize_images(path, arg):
    if path:
        # Split width and height
        crop_size = arg.split('x')
        crop_width = int(crop_size[0])
        crop_height = int(crop_size[1])

        filename = os.path.basename(str(path))
        (shortname, ext) = os.path.splitext(filename)
        cache_path = 'images/' + shortname + '-' + \
            str(crop_width) + 'x' + str(crop_height) + ext
        new_path = settings.MEDIA_ROOT + '/' + cache_path
        new_url = settings.MEDIA_URL + cache_path

        try:
            img = Image.open(settings.MEDIA_ROOT + '/images/' + filename)
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
            new_url = None

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
