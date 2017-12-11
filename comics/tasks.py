from huey.contrib.djhuey import task

from .utils.comicimporter import ComicImporter


@task()
def import_comic_files_task():
    ci = ComicImporter()
    ci.import_comic_files()
