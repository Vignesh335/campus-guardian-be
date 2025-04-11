from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Visitor
from .serializers import (
    VisitorSerializer,
    # VisitorCreateSerializer,/
    VisitorStatusSerializer
)

class VisitorViewSet(viewsets.ModelViewSet):
    queryset = Visitor.objects.all().order_by('-check_in')
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'create':
            return VisitorSerializer
        elif self.action == 'update_status':
            return VisitorStatusSerializer
        return VisitorSerializer

    # def perform_create(self, serializer):
        # if self.request.user.is_authenticated:
        #     serializer.save(host=self.request.user)
        # else:
        #     serializer.save()  # Allow anonymous creation

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        visitor = self.get_object()
        serializer = self.get_serializer(visitor, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def check_out(self, request, pk=None):
        visitor = self.get_object()
        if visitor.status != 'APPROVED':
            return Response(
                {'error': 'Only approved visitors can check out'},
                status=status.HTTP_400_BAD_REQUEST
            )
        visitor.check_out = timezone.now()
        visitor.save()
        return Response({'status': 'checked out'})