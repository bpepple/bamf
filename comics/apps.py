from django.apps import AppConfig
from django.db.models.signals import pre_delete

from comics.signals import (pre_delete_character, pre_delete_image,
                            pre_delete_issue, pre_delete_publisher)


class ComicsConfig(AppConfig):
    name = 'comics'

    def ready(self):
        arc = self.get_model('Arc')
        pre_delete.connect(pre_delete_image, sender=arc,
                           dispatch_uid='pre_delete_arc')

        creator = self.get_model('Creator')
        pre_delete.connect(pre_delete_image, sender=creator,
                           dispatch_uid='pre_delete_creator')

        team = self.get_model('Team')
        pre_delete.connect(pre_delete_image, sender=team,
                           dispatch_uid='pre_delete_team')

        character = self.get_model('Character')
        pre_delete.connect(pre_delete_character, sender=character,
                           dispatch_uid='pre_delete_character')

        publisher = self.get_model('Publisher')
        pre_delete.connect(pre_delete_publisher, sender=publisher,
                           dispatch_uid='pre_delete_publisher')

        issue = self.get_model('Issue')
        pre_delete.connect(pre_delete_issue, sender=issue,
                           dispatch_uid='pre_delete_issue')
