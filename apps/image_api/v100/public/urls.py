from rest_framework.routers import DefaultRouter

from apps.image_api.v100.views import ImageViewSet

router = DefaultRouter()
router.register(r"images", ImageViewSet, basename="image")
urlpatterns = router.urls
