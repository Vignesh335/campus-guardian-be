from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Bus, Driver, Route, Schedule, GPSLog
from .serializers import BusSerializer, DriverSerializer, RouteSerializer, ScheduleSerializer, GPSLogSerializer

class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def create(self, request, *args, **kwargs):
        # Custom logic for handling nested stop_times data during create
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save the new schedule and related stop times
            schedule = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GPSLogViewSet(viewsets.ModelViewSet):
    queryset = GPSLog.objects.all()
    serializer_class = GPSLogSerializer
