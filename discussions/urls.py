from rest_framework.routers import DefaultRouter

from discussions.views import DiscussionsViewSet

router = DefaultRouter()
router.register("discussions", DiscussionsViewSet, basename="discussions")

urlpatterns = router.urls

