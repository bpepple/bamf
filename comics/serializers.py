from rest_framework import serializers

from comics.models import Issue


class IssueListSerializer(serializers.HyperlinkedModelSerializer):
    series = serializers.StringRelatedField(many=False)
    characters = serializers.StringRelatedField(many=True)

    class Meta:
        model = Issue
        fields = ('id', 'series', 'name', 'number', 'date',
                  'status', 'desc', 'characters', 'file')
