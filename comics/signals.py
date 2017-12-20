import os.path

from django.conf import settings


def get_file(img):
    base_img = os.path.basename(img)
    new_path = settings.MEDIA_ROOT + '/images/' + base_img
    return new_path


def remove_image(img):
    if os.path.isfile(img):
        os.remove(img)


def pre_delete_image(sender, **kwargs):
    instance = kwargs['instance']

    img = get_file(instance.image)
    remove_image(img)

    thumb = get_file(instance.thumb)
    remove_image(thumb)


def pre_delete_arc(sender, **kwargs):
    instance = kwargs['instance']

    img = get_file(instance.image)
    remove_image(img)


def pre_delete_character(sender, **kwargs):
    instance = kwargs['instance']

    img = get_file(instance.image)
    remove_image(img)

    thumb = get_file(instance.thumb)
    remove_image(thumb)

    # Delete related team if this is the only
    # character related to that team.
    for team in instance.teams.all():
        if team.character_set.count() == 1:
            team.delete()


def pre_delete_publisher(sender, **kwargs):
    instance = kwargs['instance']

    logo = get_file(instance.logo)
    remove_image(logo)


def pre_delete_issue(sender, **kwargs):
    instance = kwargs['instance']

    cover = get_file(instance.cover)
    remove_image(cover)

    thumb = get_file(instance.thumb)
    remove_image(thumb)

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
