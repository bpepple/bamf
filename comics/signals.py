import os.path

from django.conf import settings

NORMAL_DIR = 'normal/'


def remove_image(img):
    if os.path.isfile(img):
        os.remove(img)


def pre_delete_arc(sender, **kwargs):
    instance = kwargs['instance']

    path = settings.MEDIA_ROOT + '/images/arcs/'
    img = path + NORMAL_DIR + str(instance.image_name())
    remove_image(img)


def pre_delete_creator(sender, **kwargs):
    instance = kwargs['instance']

    path = settings.MEDIA_ROOT + '/images/creators/'
    img = path + NORMAL_DIR + str(instance.image_name())
    remove_image(img)


def pre_delete_team(sender, **kwargs):
    instance = kwargs['instance']

    path = settings.MEDIA_ROOT + '/images/teams/'
    img = path + NORMAL_DIR + str(instance.image_name())
    remove_image(img)


def pre_delete_character(sender, **kwargs):
    instance = kwargs['instance']

    path = settings.MEDIA_ROOT + '/images/characters/'
    img = path + NORMAL_DIR + str(instance.image_name())
    remove_image(img)

    # Delete related team if this is the only
    # character related to that team.
    for team in instance.teams.all():
        if team.character_set.count() == 1:
            team.delete()


def pre_delete_publisher(sender, **kwargs):
    instance = kwargs['instance']

    path = settings.MEDIA_ROOT + '/images/publishers/'
    logo = path + NORMAL_DIR + str(instance.logo_name())
    remove_image(logo)


def pre_delete_issue(sender, **kwargs):
    instance = kwargs['instance']

    path = settings.MEDIA_ROOT + '/images/issues/'
    cover = path + NORMAL_DIR + str(instance.cover_name())
    remove_image(cover)

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
