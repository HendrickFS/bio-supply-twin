from rest_framework.routers import DefaultRouter
from .views import TransportBoxViewSet, SampleViewSet

router = DefaultRouter()
router.register(r'transport_boxes', TransportBoxViewSet, basename='transportbox')
router.register(r'samples', SampleViewSet, basename='sample')

urlpatterns = router.urls