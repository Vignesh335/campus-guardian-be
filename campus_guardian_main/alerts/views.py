from rest_framework import generics
from .models import Alert
from .serializers import AlertSerializer

class AlertListCreateView(generics.ListCreateAPIView):
    queryset = Alert.objects.all().order_by('-timestamp')
    serializer_class = AlertSerializer

class AlertDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
