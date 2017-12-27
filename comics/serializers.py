from rest_framework import serializers

from comics.models import Creator, Issue, Publisher, Series


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
