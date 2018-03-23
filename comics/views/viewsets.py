from rest_framework import viewsets, permissions
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
    permission_classes = (permissions.IsAuthenticated,)


class CharacterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Returns a list of all the characters in the database.

    read:
    Returns the information for an individual character.
    """
    queryset = (
        Character.objects
        .prefetch_related('teams')
    )
    serializer_class = CharacterSerializer
    lookup_field = 'slug'
    permission_classes = (permissions.IsAuthenticated,)


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
    permission_classes = (permissions.IsAuthenticated,)


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
        .prefetch_related('arcs', 'characters', 'teams')
    )
    serializer_class = IssueSerializer
    lookup_field = 'slug'
    permission_classes = (permissions.IsAuthenticated,)


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
    permission_classes = (permissions.IsAuthenticated,)


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
    permission_classes = (permissions.IsAuthenticated,)


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
    permission_classes = (permissions.IsAuthenticated,)
