
def pre_delete_image(sender, instance, **kwargs):
    if (instance.image):
        instance.image.delete(False)


def pre_delete_character(sender, instance, **kwargs):
    if (instance.image):
        instance.image.delete(False)

    # Delete related team if this is the only
    # character related to that team.
    for team in instance.teams.all():
        if team.character_set.count() == 1:
            team.delete()


def pre_delete_publisher(sender, instance, **kwargs):
    if (instance.logo):
        instance.logo.delete(False)


def pre_delete_issue(sender, instance, **kwargs):
    if (instance.cover):
        instance.cover.delete(False)

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
