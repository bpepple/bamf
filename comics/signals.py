import os.path


def pre_delete_image(sender, **kwargs):
    if os.path.isfile(kwargs['instance'].image):
        os.remove(kwargs['instance'].image)
        print('Remove: %s' % kwargs['instance'].image)


def pre_delete_character(sender, **kwargs):
    instance = kwargs['instance']

    # Delete object image
    if os.path.isfile(instance.image):
        os.remove(instance.image)

    # Delete related team if this is the only
    # character related to that team.
    for team in instance.teams.all():
        if team.character_set.count() == 1:
            team.delete()


def pre_delete_publisher(sender, **kwargs):
    # Delete logo image
    if os.path.isfile(kwargs['instance'].logo):
        os.remove(kwargs['instance'].logo)


def pre_delete_issue(sender, **kwargs):
    instance = kwargs['instance']

    # Delete cover image
    if os.path.isfile(instance.cover):
        os.remove(instance.cover)
        print('Removed cover: %s' % instance.cover)

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
