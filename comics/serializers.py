from rest_framework import serializers

from comics.models import Issue


class IssueListSerializer(serializers.HyperlinkedModelSerializer):
    arcs = serializers.StringRelatedField(many=True)
    characters = serializers.StringRelatedField(many=True)
    series = serializers.StringRelatedField(many=False)
    teams = serializers.StringRelatedField(many=True)

    class Meta:
        model = Issue
        fields = ('id', 'cvurl', 'series', 'name', 'number', 'date',
                  'status', 'desc', 'characters', 'teams', 'arcs', 'file', 'mod_ts')
