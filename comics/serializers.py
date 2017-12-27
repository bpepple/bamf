from rest_framework import serializers

from comics.models import (Arc, Character, Creator,
                           Issue, Publisher, Series, Team)


class IssueSerializer(serializers.HyperlinkedModelSerializer):
    arcs = serializers.StringRelatedField(many=True)
    characters = serializers.StringRelatedField(many=True)
    series = serializers.StringRelatedField(many=False)
    teams = serializers.StringRelatedField(many=True)

    class Meta:
        model = Issue
        fields = ('slug', 'cvurl', 'series', 'name', 'number', 'date',
                  'status', 'desc', 'characters', 'teams', 'arcs', 'file', 'mod_ts')
        lookup_field = 'slug'


class PublisherSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Publisher
        fields = ('slug', 'cvurl', 'name', 'desc')
        lookup_field = 'slug'


class SeriesSerializer(serializers.HyperlinkedModelSerializer):
    publisher = serializers.StringRelatedField(many=False)

    class Meta:
        model = Series
        fields = ('slug', 'cvurl', 'name', 'sort_title',
                  'publisher', 'year', 'desc')
        lookup_field = 'slug'


class CreatorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Creator
        fields = ('slug', 'cvurl', 'name', 'desc')
        lookup_field = 'slug'


class CharacterSerializer(serializers.HyperlinkedModelSerializer):
    teams = serializers.StringRelatedField(many=True)

    class Meta:
        model = Character
        fields = ('slug', 'cvurl', 'name', 'teams', 'desc')
        lookup_field = 'slug'


class TeamSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Team
        fields = ('slug', 'cvurl', 'name', 'desc')
        lookup_field = 'slug'


class ArcSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Arc
        fields = ('slug', 'cvurl', 'name', 'desc')
        lookup_field = 'slug'
