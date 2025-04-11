from rest_framework import viewsets, permissions
from .models import Lecturer
from .serializers import LecturerSerializer

class LecturerViewSet(viewsets.ModelViewSet):
    queryset = Lecturer.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = LecturerSerializer
    filterset_fields = ['type', 'department_name', 'is_active']
    search_fields = ['display_name', 'staff_id', 'specialization']

    def perform_create(self, serializer):
        serializer.save()