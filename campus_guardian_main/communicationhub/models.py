from django.db import models

from campus_guardian_main.users.models import User


class VoiceText(models.Model):
    # management = models.ForeignKey('management.Lecturer', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='voice_texts', null=True)
    title = models.CharField(max_length=255, null=False, default="")
    audio_file = models.FileField(upload_to='voice_uploads/')
    transcription = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"


class Feedback(models.Model):
    COMPLAINT = 'complaint'
    COMPLIMENT = 'compliment'
    QUESTION = 'question'
    SUGGESTION= 'suggestion'

    CATEGORY_CHOICES = [
        (COMPLAINT, 'Complaint'),
        (SUGGESTION, 'Suggestion'),
        (COMPLIMENT, 'Compliment'),
        (QUESTION, 'Question'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks', null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    feedback_text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username} on {self.created_at}"

class Reply(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    reply_text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user.username if self.user else 'Anonymous'} to Feedback {self.feedback.id}"

class Announcement(models.Model):
    CATEGORY_CHOICES = [
        ("meeting", "Meeting"),
        ("policy", "Policy"),
        ("maintenance", "Maintenance"),
    ]
    URGENCY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    content = models.TextField()
    sender = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    urgency = models.CharField(max_length=50, choices=URGENCY_CHOICES)
    has_response = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender}: {self.content[:30]}..."