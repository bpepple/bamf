import base64
import imghdr
import io

from PIL import Image

from comics.models import Issue

from .comicapi.comicarchive import ComicArchive


class ImageAPIHandler(object):

    def getContentType(self, image_data):
        img = 'jpg'
        imtype = imghdr.what(None, image_data)
        if imtype is not None:
            return imtype

        return img

    def getImageData(self, slug, pagenum):
        image_data = None
        obj = Issue.objects.get(slug=slug)

        if obj is not None:
            if int(pagenum) < obj.page_count:
                ca = ComicArchive(obj.file)
                image_data = ca.getPage(int(pagenum))
        # TODO: Set a default image if no image if found.

        return image_data

    def resizeImage(self, max_height, image_data):
        i = Image.open(io.BytesIO(image_data))
        w, h = i.size
        if max_height < h:
            i.thumbnail((w, max), Image.ANTIALIAS)
            output = io.BytesIO()
            i.save(output, format='JPEG')
            return output.getvalue()
        else:
            return image_data

    def get_uri(self, slug, pagenum):
        image_data = self.getImageData(slug, pagenum)
        image_type = self.getContentType(image_data)
        base64_data = base64.b64encode(image_data).decode('ascii')
        uri = 'data:%s;base64,%s' % (image_type, base64_data)

        return uri
