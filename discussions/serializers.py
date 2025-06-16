from rest_framework import serializers

from discussions.models import Discussion


class DiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields = ['id', 'creator', 'title', 'created_at', 'updated_at']