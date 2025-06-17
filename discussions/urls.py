from rest_framework.routers import DefaultRouter

from discussions.views import DiscussionsViewSet, CommentsViewSet

router = DefaultRouter()

router.register("discussions", DiscussionsViewSet, basename="discussions")
router.register("comments", CommentsViewSet, basename="comments")

urlpatterns = router.urls
