import base64
import imghdr
import io

from PIL import Image

from .comicapi.comicarchive import ComicArchive


class ImageAPIHandler(object):

    def getContentType(self, image_data):
        img = 'jpg'
        imtype = imghdr.what(None, image_data)
        if imtype is not None:
            return imtype

        return img

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

    def get_uri(self, issue_file, page_num):
        ca = ComicArchive(issue_file)
        image_data = ca.getPage(int(page_num))
        image_type = self.getContentType(image_data)
        base64_data = base64.b64encode(image_data).decode('ascii')
        uri = 'data:%s;base64,%s' % (image_type, base64_data)

        return uri
