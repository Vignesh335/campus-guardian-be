from rest_framework import generics
from .models import VoiceText, Feedback, Reply, Announcement
from .serializers import VoiceTextSerializer, FeedbackSerializer,ReplySerializer, AnnouncementSerializer

class VoiceTextCreateView(generics.CreateAPIView):
    queryset = VoiceText.objects.all()
    serializer_class = VoiceTextSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class VoiceTextListView(generics.ListAPIView):
    queryset = VoiceText.objects.all()
    serializer_class = VoiceTextSerializer

class AnnouncementListCreateView(generics.ListCreateAPIView):
    queryset = Announcement.objects.all().order_by('-timestamp')
    serializer_class = AnnouncementSerializer

class AnnouncementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer


class FeedbackListCreateView(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def perform_create(self, serializer):
        # Set the user from the request context (authenticated user)
        serializer.save(user=self.request.user)


class ReplyCreateView(generics.CreateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)