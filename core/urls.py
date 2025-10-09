from rest_framework.routers import DefaultRouter
from .views import (
    TransportBoxViewSet,
    SampleViewSet,
    TelemetryReadingViewSet,
    SLAConfigViewSet,
    AlertViewSet,
)

router = DefaultRouter()
router.register(r'transport_boxes', TransportBoxViewSet, basename='transportbox')
router.register(r'samples', SampleViewSet, basename='sample')
router.register(r'telemetry', TelemetryReadingViewSet, basename='telemetry')
router.register(r'sla', SLAConfigViewSet, basename='slaconfig')
router.register(r'alerts', AlertViewSet, basename='alert')

urlpatterns = router.urls