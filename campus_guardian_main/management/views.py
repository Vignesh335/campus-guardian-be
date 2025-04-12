from rest_framework import viewsets, permissions

from rest_framework.decorators import action
from .models import Lecturer, Attendance
from rest_framework.response import Response
from calendar import monthrange
from datetime import datetime, date
from .serializers import LecturerSerializer, AttendanceSerializer


class LecturerViewSet(viewsets.ModelViewSet):
    queryset = Lecturer.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = LecturerSerializer
    filterset_fields = ['type', 'department_name', 'is_active']
    search_fields = ['display_name', 'staff_id', 'specialization']

    def perform_create(self, serializer):
        serializer.save()


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related('lecturer').all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Get the filters from the query parameters
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        day = self.request.query_params.get('day')
        lecturer_id = self.request.query_params.get('lecturer_id')
        department = self.request.query_params.get('department')

        queryset = Attendance.objects.select_related('lecturer')

        # Apply filtering by year, month, and day if provided
        if year:
            try:
                year = int(year)
                queryset = queryset.filter(date__year=year)
            except ValueError:
                pass  # If the year is invalid, we just return all records

        if month:
            try:
                month = int(month)
                queryset = queryset.filter(date__month=month)
            except ValueError:
                pass  # If the month is invalid, we just return all records

        if day:
            try:
                day = int(day)
                queryset = queryset.filter(date__day=day)
            except ValueError:
                pass  # If the day is invalid, we just return all records

        # Apply filtering by lecturer ID if provided
        if lecturer_id:
            try:
                lecturer_id = int(lecturer_id)
                queryset = queryset.filter(lecturer_id=lecturer_id)
            except ValueError:
                pass  # If the lecturer_id is invalid, we just return all records

        # Apply filtering by department if provided
        if department:
            queryset = queryset.filter(lecturer__department__icontains=department)

        return queryset

    @action(detail=False, methods=['get'], url_path='daily-summary')
    def daily_summary(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        lecturer = request.query_params.get('lecturer')
        department = request.query_params.get('department')

        if not year or not month:
            return Response({"error": "Year and month are required"}, status=400)

        try:
            year = int(year)
            month = int(month)
        except ValueError:
            return Response({"error": "Invalid year or month"}, status=400)

        # Get number of days in the month
        num_days = monthrange(year, month)[1]
        summary_data = []

        for day in range(1, num_days + 1):
            day_date = date(year, month, day)
            queryset = Attendance.objects.filter(date=day_date)

            if lecturer:
                queryset = queryset.filter(lecturer_id=lecturer)
            if department:
                queryset = queryset.filter(lecturer__department__iexact=department)

            present = queryset.filter(status='pr').count()
            late = queryset.filter(status='late').count()
            absent = queryset.filter(status='ab').count()
            total = queryset.count() or 1

            summary_data.append({
                "date": day_date,
                "presentCount": present,
                "lateCount": late,
                "absentCount": absent,
                "presentPercentage": round((present / total) * 100, 1),
                "latePercentage": round((late / total) * 100, 1),
                "absentPercentage": round((absent / total) * 100, 1),
            })

        return Response(summary_data)

# views.py
# import json
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_POST, require_GET
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import get_object_or_404
# from webauthn import (
#     generate_registration_options,
#     verify_registration_response,
#     generate_authentication_options,
#     verify_authentication_response,
#     options_to_json,
# )
# from webauthn.helpers.structs import PublicKeyCredentialDescriptor, UserVerificationRequirement
# from .models import Lecturer, WebAuthnCredential
#
#
# @login_required
# @require_GET
# def begin_registration(request):
#     lecturer_id = request.GET.get('lecturer_id')
#     lecturer = get_object_or_404(Lecturer, id=lecturer_id)
#
#     # Generate registration options
#     options_json, _ = prepare_registration_options(lecturer)
#
#     return JsonResponse(json.loads(options_json))
#
#
# @csrf_exempt
# @require_POST
# def complete_registration(request):
#     data = json.loads(request.body)
#     lecturer_id = data.get('lecturer_id')
#     attestation = data.get('attestation')
#
#     lecturer = get_object_or_404(Lecturer, id=lecturer_id)
#     challenge = get_challenge_for_user(lecturer.id)
#
#     if not challenge:
#         return JsonResponse({'error': 'Challenge expired or not found'}, status=400)
#
#     try:
#         # Verify the registration response
#         verification = verify_registration_response(
#             credential=attestation,
#             expected_challenge=challenge,
#             expected_origin=get_origin(request),
#             expected_rp_id=RP_ID
#         )
#
#         # Convert binary credential_id to string for storage
#         credential_id_str = bytes_to_base64url(verification.credential_id)
#
#         # Save the credential
#         WebAuthnCredential.objects.create(
#             lecturer=lecturer,
#             credential_id=credential_id_str,  # Now storing as a string
#             public_key=verification.credential_public_key,
#             sign_count=verification.sign_count,
#             credential_name=data.get('credential_name', 'Fingerprint')
#         )
#
#         # Update the lecturer model
#         lecturer.webauthn_enabled = True
#         lecturer.save()
#
#         return JsonResponse({'success': True})
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=400)
#
#
# @require_GET
# def begin_authentication(request):
#     email = request.GET.get('email')
#     lecturer = get_object_or_404(Lecturer, email=email)
#
#     if not lecturer.webauthn_enabled:
#         return JsonResponse({'error': 'WebAuthn not enabled for this user'}, status=400)
#
#     # Get stored credentials
#     credentials = lecturer.credentials.all()
#     allowed_credentials = []
#
#     for cred in credentials:
#         # Convert stored string credential_id back to binary
#         binary_credential_id = base64url_to_bytes(cred.credential_id)
#         allowed_credentials.append(
#             PublicKeyCredentialDescriptor(id=binary_credential_id)
#         )
#
#     challenge = generate_challenge()
#     store_challenge_for_user(lecturer.id, challenge)
#
#     options = generate_authentication_options(
#         rp_id=RP_ID,
#         challenge=challenge,
#         allow_credentials=allowed_credentials,
#         user_verification=UserVerificationRequirement.PREFERRED
#     )
#
#     return JsonResponse(json.loads(options_to_json(options)))
#
#
# @csrf_exempt
# @require_POST
# def complete_authentication(request):
#     data = json.loads(request.body)
#     email = data.get('email')
#     assertion = data.get('assertion')
#
#     lecturer = get_object_or_404(Lecturer, email=email)
#     challenge = get_challenge_for_user(lecturer.id)
#
#     if not challenge:
#         return JsonResponse({'error': 'Challenge expired or not found'}, status=400)
#
#     try:
#         # The credential ID is already a string from the client
#         credential_id_str = assertion['id']
#         stored_credential = get_object_or_404(WebAuthnCredential, credential_id=credential_id_str)
#
#         # For verification, we need to convert the client's response
#         # Client sends base64url strings which need conversion for the verification library
#         assertion_for_verification = assertion.copy()
#         assertion_for_verification['rawId'] = base64url_to_bytes(assertion['id'])
#
#         # Verify the authentication response
#         verification = verify_authentication_response(
#             credential=assertion_for_verification,
#             expected_challenge=challenge,
#             expected_origin=get_origin(request),
#             expected_rp_id=RP_ID,
#             credential_public_key=stored_credential.public_key,
#             credential_current_sign_count=stored_credential.sign_count
#         )
#
#         # Update the sign count
#         stored_credential.sign_count = verification.new_sign_count
#         stored_credential.save()
#
#         # Return a success response with authentication token
#         # You should generate a proper auth token here
#         return JsonResponse({
#             'success': True,
#             'user': {
#                 'id': lecturer.id,
#                 'name': lecturer.display_name,
#                 'email': lecturer.email,
#                 'staff_id': lecturer.staff_id
#             },
#             'token': 'your-auth-token-here'  # Replace with proper token generation
#         })
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=400)
#
#
# @login_required
# @require_GET
# def list_credentials(request, lecturer_id):
#     lecturer = get_object_or_404(Lecturer, id=lecturer_id)
#     credentials = lecturer.credentials.all()
#
#     return JsonResponse({
#         'credentials': [
#             {
#                 'id': cred.credential_id,  # Already a string
#                 'name': cred.credential_name,
#                 'created_at': cred.created_at.isoformat()
#             }
#             for cred in credentials
#         ]
#     })
#
#
# @csrf_exempt
# @login_required
# @require_POST
# def delete_credential(request):
#     data = json.loads(request.body)
#     credential_id_str = data.get('credential_id')  # Already a string
#
#     credential = get_object_or_404(WebAuthnCredential, credential_id=credential_id_str)
#     credential.delete()
#
#     # If this was the last credential, disable WebAuthn for the user
#     lecturer = credential.lecturer
#     if not lecturer.credentials.exists():
#         lecturer.webauthn_enabled = False
#         lecturer.save()
#
#     return JsonResponse({'success': True})