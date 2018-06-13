from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from comics.tasks import import_comic_files_task


@login_required
def importer(request):
    import_comic_files_task.apply_async()
    return HttpResponseRedirect('/')
