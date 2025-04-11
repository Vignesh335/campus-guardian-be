from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('create/', views.create_notification, name='create_notification'),
    path('approve/<int:notification_id>/', views.approve_notification, name='approve_notification'),
    path('deny/<int:notification_id>/', views.deny_notification, name='deny_notification'),
    # path('approve/<int:notification_id>/', views.approve_notification, name='approve_notification'),
]
