from rest_framework import serializers

from discussions.models import Discussion, Comment


class DiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields = ['id', 'creator', 'title', 'created_at', 'updated_at']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'discussion', 'parent', 'content', 'created_at', 'updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        author_data = {
            "author_id": instance.author.id,
            "author_name": instance.author.username
        }

        representation.update(author_data)

        return representation

