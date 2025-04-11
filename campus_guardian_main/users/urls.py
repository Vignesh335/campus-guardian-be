from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UsersViewSet

router = DefaultRouter()
router.register(r'', UsersViewSet, basename='visitor')

urlpatterns = [
    path('', include(router.urls)),
]