import os.path

from django.conf import settings


LARGE_THUMB = '-320x487'
SMALL_THUMB = '-200x305'


def remove_images(img):
    if os.path.isfile(img):
        os.remove(img)

        original_img = os.path.basename(img)
        (shortname, ext) = os.path.splitext(original_img)

        thumb_cache = settings.MEDIA_ROOT + '/CACHE/'
        small_thumb = thumb_cache + shortname + SMALL_THUMB + ext
        large_thumb = thumb_cache + shortname + LARGE_THUMB + ext

        if os.path.isfile(small_thumb):
            os.remove(small_thumb)
        if os.path.isfile(large_thumb):
            os.remove(large_thumb)


def pre_delete_image(sender, **kwargs):
    remove_images(kwargs['instance'].image)


def pre_delete_character(sender, **kwargs):
    instance = kwargs['instance']

    remove_images(instance.image)

    # Delete related team if this is the only
    # character related to that team.
    for team in instance.teams.all():
        if team.character_set.count() == 1:
            team.delete()


def pre_delete_publisher(sender, **kwargs):
    remove_images(kwargs['instance'].logo)


def pre_delete_issue(sender, **kwargs):
    instance = kwargs['instance']

    remove_images(instance.cover)

    # Delete related arc if this is the only
    # issue related to that arc.
    for arc in instance.arcs.all():
        if arc.issue_set.count() == 1:
            arc.delete()

    # Delete related character if this is the only
    # issue related to that character.
    for character in instance.characters.all():
        if character.issue_set.count() == 1:
            character.delete()

    # Delete related team if this is the only
    # issue related to that team.
    for team in instance.teams.all():
        if team.issue_set.count() == 1:
            team.delete()
