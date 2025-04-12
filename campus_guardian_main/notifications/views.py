# notifications/views.py
# from django.contrib.sites import requests
import requests
from django.core.mail import send_mail
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Notification
import json

from ..management.models import Lecturer
from ..visitors.models import Visitor


@csrf_exempt
def create_notification(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Get Management and Visitor instances
            management = get_object_or_404(Lecturer, id=data['management_id'])
            visitor = get_object_or_404(Visitor, id=data['visitor_id'])
            print(management.email)

            # Create Notification
            notification = Notification.objects.create(
                management=management,
                visitor=visitor,
                title=data['title'],
                message=data['message'],
                # email=management.email
            )

            # Create approval URL
            approve_url = request.build_absolute_uri(
                reverse('notifications:approve_notification', args=[notification.id])
            )
            deny_url = request.build_absolute_uri(
                reverse('notifications:deny_notification', args=[notification.id])
            )

            # Create the HTML email content
            html_message = f"""
                <p><strong>{notification.title}</strong></p>
                <p>{notification.message}</p>
                <p><strong>Visitor:</strong> {visitor.name}</p>
                <p><strong>To (Management):</strong> {management.display_name}</p>
                <p>
                    <a href="{approve_url}" style="display:inline-block;padding:10px 15px;background-color:#4CAF50;color:white;text-decoration:none;border-radius:5px;">
                        Approve
                    </a>
                </p>
                <p>
                    <a href="{deny_url}" style="display:inline-block;padding:10px 15px;background-color:#4CAF50;color:white;text-decoration:none;border-radius:5px;">
                        Deny
                    </a>
                </p>
            """

            # Send the email
            send_mail(
                subject='Approval Required: Visitor Notification',
                message=notification.message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=["koyiladavignesh@gmail.com"],
                html_message=html_message
            )

            return JsonResponse({'status': 'Notification created and email sent'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)


def approve_notification(request, notification_id):
    # Retrieve the notification based on the ID, handle 404 errors gracefully
    notification = get_object_or_404(Notification, id=notification_id)
    visitor = notification.visitor

    # Define the API endpoint for updating the visitor's status
    url = f"http://127.0.0.1:8000/api/visitors/{visitor.id}/update_status/"

    # Define the data you want to send in the PATCH request
    data = {
        "status": "APPROVED",  # Change this to "APPROVED" if needed
        "denial_reason": ""
    }

    try:
        # Make a PATCH request to the visitor API to update the status
        response = requests.patch(url, json=data)

        # Check if the request was successful (status code 200 or 204)
        if response.status_code == 200 or response.status_code == 204:
            # Successfully updated the visitor's status
            return JsonResponse({"message": "Notification approved and status updated successfully."}, status=200)
        else:
            # Provide more information in case of failure (e.g., error message from visitor API)
            return JsonResponse({"message": f"Failed to update visitor status. Error: {response.text}"}, status=400)
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request (e.g., network issues)
        return JsonResponse({"message": f"An error occurred while communicating with the visitor API: {str(e)}"},
                            status=500)

def deny_notification(request, notification_id):
    # Retrieve the notification based on the ID, handle 404 errors gracefully
    notification = get_object_or_404(Notification, id=notification_id)
    visitor = notification.visitor

    # Define the API endpoint for updating the visitor's status
    url = f"http://127.0.0.1:8000/api/visitors/{visitor.id}/update_status/"

    # Define the data you want to send in the PATCH request
    data = {
        "status": "DENIED",  # Change this to "APPROVED" if needed
        "denial_reason": "No available appointment slot"
    }

    try:
        # Make a PATCH request to the visitor API to update the status
        response = requests.patch(url, json=data)

        # Check if the request was successful (status code 200 or 204)
        if response.status_code == 200 or response.status_code == 204:
            # Successfully updated the visitor's status
            return JsonResponse({"message": "Notification denied and status updated successfully."}, status=200)
        else:
            # Provide more information in case of failure (e.g., error message from visitor API)
            return JsonResponse({"message": f"Failed to update visitor status. Error: {response.text}"}, status=400)
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request (e.g., network issues)
        return JsonResponse({"message": f"An error occurred while communicating with the visitor API: {str(e)}"},
                            status=500)