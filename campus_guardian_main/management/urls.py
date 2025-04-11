from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LecturerViewSet

router = DefaultRouter()
router.register(r'', LecturerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]