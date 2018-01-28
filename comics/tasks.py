from huey.contrib.djhuey import task

from .utils.comicimporter import ComicImporter


@task()
def import_comic_files_task():
    ci = ComicImporter()
    ci.import_comic_files()
    return


@task()
def refresh_issue_task(cvid):
    ci = ComicImporter()
    success = ci.refreshIssueData(cvid)
    return success
