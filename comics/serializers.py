from rest_framework import serializers

from comics.models import (Arc, Character, Creator,
                           Issue, Publisher, Series, Team)


class IssueSerializer(serializers.HyperlinkedModelSerializer):
    arcs = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='api:arc-detail', lookup_field='slug')
    characters = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='api:character-detail', lookup_field='slug')
    series = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name='api:series-detail', lookup_field='slug')
    teams = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='api:team-detail', lookup_field='slug')

    class Meta:
        model = Issue
        fields = ('slug', 'cvurl', 'series', 'name', 'number', 'date',
                  'page_count', 'status', 'desc', 'characters', 'teams', 'arcs', 'cover')
        lookup_field = 'slug'


class PublisherSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Publisher
        fields = ('slug', 'cvurl', 'name', 'desc', 'logo')
        lookup_field = 'slug'


class SeriesSerializer(serializers.HyperlinkedModelSerializer):
    publisher = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name='api:publisher-detail', lookup_field='slug')

    class Meta:
        model = Series
        fields = ('slug', 'cvurl', 'name', 'sort_title',
                  'publisher', 'year', 'desc')
        lookup_field = 'slug'


class CreatorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Creator
        fields = ('slug', 'cvurl', 'name', 'desc', 'image')
        lookup_field = 'slug'


class CharacterSerializer(serializers.HyperlinkedModelSerializer):
    teams = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='api:team-detail', lookup_field='slug')

    class Meta:
        model = Character
        fields = ('slug', 'cvurl', 'name', 'teams', 'desc', 'image')
        lookup_field = 'slug'


class TeamSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Team
        fields = ('slug', 'cvurl', 'name', 'desc', 'image')
        lookup_field = 'slug'


class ArcSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Arc
        fields = ('slug', 'cvurl', 'name', 'desc', 'image')
        lookup_field = 'slug'
