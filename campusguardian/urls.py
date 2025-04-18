# from django.contrib import admin
from django.urls import path, include
# from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('api/visitors/', include('campus_guardian_main.visitors.urls')),
    path('api/notifications/', include('campus_guardian_main.notifications.urls', namespace='notifications')),
    path('api/users/', include('campus_guardian_main.users.urls')),
    path('api/bus_tracker/', include('campus_guardian_main.bus_tracker.urls')),
    path('api/communication/', include('campus_guardian_main.communicationhub.urls')),
    path('api/', include('campus_guardian_main.management.urls')),
    path('api/alerts/', include('campus_guardian_main.alerts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

