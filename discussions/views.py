from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from discussions.models import Discussion
from discussions.serializers import DiscussionSerializer


class DiscussionsViewSet(
    GenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
):

    queryset = Discussion.objects.all().order_by('-created_at')
    serializer_class = DiscussionSerializer

    @action(detail=True, methods=['post'], url_path="delete")
    def delete_discussion(self, request, pk=None):
        discussion = self.get_object()
        creator_id = request.data.get("creator")

        if not creator_id:
            return Response({"detail": "Missing creator field"}, status=status.HTTP_400_BAD_REQUEST)

        if str(discussion.creator_id) != str(creator_id):
            raise PermissionDenied("You are not allowed to delete this discussion.")

        discussion.delete()
        return Response({"detail": "Discussion deleted."}, status=status.HTTP_204_NO_CONTENT)
