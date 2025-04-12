from django.urls import path
from .views import VoiceTextCreateView, VoiceTextListView,FeedbackListCreateView, ReplyCreateView, AnnouncementListCreateView, AnnouncementDetailView

urlpatterns = [
    path('upload/', VoiceTextCreateView.as_view(), name='voice-text-upload'),
    path('list/', VoiceTextListView.as_view(), name='voice-text-list'),
    path('feedbacks/', FeedbackListCreateView.as_view(), name='feedback-list-create'),
    path('replies/', ReplyCreateView.as_view(), name='reply-create'),
    path('announcements/', AnnouncementListCreateView.as_view(), name='announcement-list-create'),
    path('announcements/<int:pk>/', AnnouncementDetailView.as_view(), name='announcement-detail'),
]
