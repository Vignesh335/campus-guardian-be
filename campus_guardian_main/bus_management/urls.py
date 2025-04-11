from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusViewSet, DriverViewSet, RouteViewSet, BusScheduleViewSet, BusLocationViewSet, \
    CombinedBusDataViewSet

router = DefaultRouter()
router.register(r'buses', BusViewSet, basename='bus')
router.register(r'drivers', DriverViewSet, basename='driver')
router.register(r'routes', RouteViewSet, basename='route')
router.register(r'schedules', BusScheduleViewSet, basename='schedule')
router.register(r'locations', BusLocationViewSet, basename='location')
router.register(r'bus_data', CombinedBusDataViewSet, basename='bus_data')

urlpatterns = [
    path('', include(router.urls)),
]