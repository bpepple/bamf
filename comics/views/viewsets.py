from rest_framework import viewsets
from comics.serializers import (ArcSerializer, CharacterSerializer,
                                CreatorSerializer, IssueSerializer,
                                PublisherSerializer, SeriesSerializer,
                                TeamSerializer)
from comics.models import (Arc, Character, Creator,
                           Issue, Publisher, Series,
                           Team)


class ArcViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Returns a list of all the story arcs in the database.

    read:
    Returns the information of an individual story arc.
    """
    queryset = Arc.objects.all()
    serializer_class = ArcSerializer
    lookup_field = 'slug'


class CharacterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Returns a list of all the characters in the database.

    read:
    Returns the information for an individual character.
    """
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    lookup_field = 'slug'


class CreatorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Returns a list of all creators in the database.

    read:
    Returns the information of an individual creator.
    """
    queryset = Creator.objects.all()
    serializer_class = CreatorSerializer
    lookup_field = 'slug'


class IssueViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Returns a list of all issues in the database.

    read:
    Returns the information of an individual issue.
    """
    queryset = (
        Issue.objects
        .select_related('series')
        .prefetch_related('characters')
        .prefetch_related('teams')
        .prefetch_related('arcs')
    )
    serializer_class = IssueSerializer
    lookup_field = 'slug'


class PublisherViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Returns a list of all publishers.

    read:
    Returns the information of an individual publisher.
    """
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    lookup_field = 'slug'


class SeriesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Returns a list of all the comic series.

    read:
    Returns the information of an individual comic series.
    """
    queryset = (
        Series.objects
        .select_related('publisher')
    )
    serializer_class = SeriesSerializer
    lookup_field = 'slug'


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Returns a list of all the teams in the database.

    read:
    Returns the information for an individual team.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    lookup_field = 'slug'
