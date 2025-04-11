from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusViewSet, DriverViewSet, RouteViewSet, ScheduleViewSet, GPSLogViewSet

router = DefaultRouter()
router.register(r'buses', BusViewSet)
router.register(r'drivers', DriverViewSet)
router.register(r'routes', RouteViewSet)
router.register(r'schedules', ScheduleViewSet)
router.register(r'gpslogs', GPSLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
