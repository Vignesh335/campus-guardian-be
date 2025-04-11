from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/visitors/', include('campus_guardian_main.visitors.urls')),
    path('api/notifications/', include('campus_guardian_main.notifications.urls', namespace='notifications')),
    path('api/users/', include('campus_guardian_main.users.urls')),
    path('api/bus_track/', include('campus_guardian_main.bus_management.urls')),
    path('api/management/', include('campus_guardian_main.management.urls')),
    # path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

