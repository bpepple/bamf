import os.path

from django.conf import settings

from os import remove


def get_file(img):
    base_img = os.path.basename(img)
    new_path = settings.MEDIA_ROOT + '/images/' + base_img
    return new_path


def pre_delete_image(sender, **kwargs):
    instance = kwargs['instance']
    img = get_file(instance.image)
    if os.path.isfile(img):
        remove(img)
    thumb = get_file(instance.thumb)
    if os.path.isfile(thumb):
        remove(thumb)


def pre_delete_arc(sender, **kwargs):
    instance = kwargs['instance']
    img = get_file(instance.image)
    if os.path.isfile(img):
        remove(img)


def pre_delete_character(sender, **kwargs):
    instance = kwargs['instance']
    img = get_file(instance.image)
    if os.path.isfile(img):
        remove(img)
    thumb = get_file(instance.thumb)
    if os.path.isfile(thumb):
        remove(thumb)

    # Delete related team if this is the only
    # character related to that team.
    for team in instance.teams.all():
        if team.character_set.count() == 1:
            team.delete()


def pre_delete_publisher(sender, **kwargs):
    instance = kwargs['instance']
    logo = get_file(instance.logo)
    if os.path.isfile(logo):
        remove(logo)


def pre_delete_issue(sender, **kwargs):
    instance = kwargs['instance']
    cover = get_file(instance.cover)
    if os.path.isfile(cover):
        remove(cover)
    thumb = get_file(instance.thumb)
    if os.path.isfile(thumb):
        remove(thumb)

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
