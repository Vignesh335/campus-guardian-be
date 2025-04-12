# from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import LecturerViewSet, webauthn_registration_options, webauthn_registration_verify, \
#     webauthn_authentication_options, webauthn_authentication_verify
#
# router = DefaultRouter()
#
# urlpatterns = [
#     path('webauthn/registration/options/', webauthn_registration_options, name='webauthn_registration_options'),
#     path('', include(router.urls)),
#     path('webauthn/registration/verify/', webauthn_registration_verify, name='webauthn_registration_verify'),
#
#     # Authentication flow
#     path('webauthn/authentication/options/', webauthn_authentication_options, name='webauthn_authentication_options'),
#     path('webauthn/authentication/verify/', webauthn_authentication_verify, name='webauthn_authentication_verify'),
# ]
# urls.py
from django.urls import path, include
from . import views
# DailyAttendanceSummary = views.DailyAttendanceSummary

# from .views import (
#     # lecturer_registration,
#     webauthn_registration_options,
#     webauthn_registration_verify, LecturerViewSet, webauthn_authentication_verify, webauthn_authentication_options,
# # webauthn_authentication_verify
# )

router = DefaultRouter()

router.register(r'management', views.LecturerViewSet)
router.register(r'attendance', views.AttendanceViewSet)
# router.register(r"daily-summary", DailyAttendanceSummary)

urlpatterns = [
    path('', include(router.urls)),
    # path('register/lecturer/', views.lecturer_registration, name='lecturer-registration'),
    # WebAuthn Registration
    # path('webauthn/register/begin/', views.begin_registration, name='webauthn_begin_register'),
    # path('webauthn/register/complete/', views.complete_registration, name='webauthn_complete_register'),
    #
    # # WebAuthn Authentication
    # path('webauthn/authenticate/begin/', views.begin_authentication, name='webauthn_begin_auth'),
    # path('webauthn/authenticate/complete/', views.complete_authentication, name='webauthn_complete_auth'),
    #
    # # Credential Management
    # path('webauthn/credentials/<int:lecturer_id>/', views.list_credentials, name='webauthn_list_credentials'),
    # path('webauthn/credentials/delete/', views.delete_credential, name='webauthn_delete_credential'),
    # path('register/webauthn/options/', webauthn_registration_options, name='webauthn-registration-options'),
    # path('register/webauthn/verify/', webauthn_registration_verify, name='webauthn-registration-verify'),
    # path('webauthn/authenticate/options/', webauthn_authentication_options,
    #      name='webauthn_authentication_options'),
    # path('webauthn/authenticate/verify/', webauthn_authentication_verify, name='webauthn_authentication_verify'),
]