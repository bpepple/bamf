from django.http import HttpResponseRedirect

from comics.tasks import import_comic_files_task


def importer(request):
    import_comic_files_task()
    return HttpResponseRedirect('/')
