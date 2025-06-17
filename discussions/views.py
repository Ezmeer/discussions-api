from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, ListModelMixin, DestroyModelMixin, \
    UpdateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from discussions.mixins import OwnerPermissionMixin
from discussions.models import Discussion, Comment
from discussions.serializers import DiscussionSerializer, CommentSerializer


class DefaultPagination(PageNumberPagination):
    page_size = 10


class DiscussionsViewSet(
    OwnerPermissionMixin,
    GenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
):

    queryset = Discussion.objects.all().order_by('-created_at')
    serializer_class = DiscussionSerializer
    pagination_class = DefaultPagination

    @action(detail=True, methods=['post'], url_path="delete")
    def delete_discussion(self, request, pk=None):
        discussion = self.get_object()
        creator_id = request.data.get("creator")

        self.assert_is_owner(discussion, "creator_id", creator_id)

        discussion.delete()
        return Response({"detail": "Discussion deleted."}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path="update")
    def update_title(self, request, pk=None):
        discussion = self.get_object()
        creator_id = request.data.get("creator")

        self.assert_is_owner(discussion, "creator_id", creator_id)

        discussion.title = request.data.get('title')
        discussion.save(update_fields=['title'])

        serializer = self.serializer_class(discussion)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentsViewSet(
    OwnerPermissionMixin,
    GenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
):

    queryset = Comment.objects.all().select_related('author').order_by('-created_at')
    serializer_class = CommentSerializer
    pagination_class = DefaultPagination

    def create(self, request, *args, **kwargs):
        author_id = request.data.get("author")
        discussion_id = request.data.get("discussion")
        parent_id = request.data.get("parent")
        content = request.data.get("content")

        if not author_id or not discussion_id or not content:
            return Response({"detail": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            comment = Comment.objects.create(
                author_id=author_id,
                discussion_id=discussion_id,
                parent_id=parent_id,
                content=content
            )
        except IntegrityError:
            raise ValidationError({"detail": "Invalid foreign key."})

        serializer = self.get_serializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        discussion_id = request.query_params.get('discussion_id')

        if not discussion_id:
            Response({"detail": "Missing discussion id field"}, status=status.HTTP_400_BAD_REQUEST)

        comments = self.queryset.filter(discussion_id=discussion_id, parent__isnull=True)

        paginated_comments = self.paginate_queryset(comments)
        serializer = self.get_serializer(paginated_comments, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['get'])
    def replies(self, request, pk=None):
        parent_comment = self.get_object()

        replies = self.queryset.filter(parent=parent_comment)

        paginated_replies = self.paginate_queryset(replies)
        serializer = self.get_serializer(paginated_replies, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post'], url_path="delete")
    def delete_comment(self, request, pk=None):
        comment = self.get_object()
        creator_id = request.data.get("creator")

        self.assert_is_owner(comment, "creator_id", creator_id)

        comment.delete()
        return Response({"detail": "Discussion deleted."}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path="update")
    def update_content(self, request, pk=None):
        comment = self.get_object()
        creator_id = request.data.get("creator")

        self.assert_is_owner(comment, "creator_id", creator_id)

        comment.content = request.data.get('content')
        comment.save(update_fields=['content'])

        serializer = self.serializer_class(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
