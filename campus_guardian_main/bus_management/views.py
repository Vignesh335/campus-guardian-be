from django.db.models import Prefetch, Subquery, OuterRef
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from django.db import connection
from rest_framework.response import Response
from .models import Bus, Driver, Route, BusSchedule, BusLocationHistory
from .serializers import BusSerializer, DriverSerializer, RouteSerializer, BusScheduleSerializer, BusLocationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class CombinedBusDataViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        try:
            # Get all buses with their drivers and schedules
            buses = Bus.objects.select_related(
                'driver',
                'driver__user'
            ).prefetch_related(
                Prefetch(
                    'schedules',
                    queryset=BusSchedule.objects.select_related('route')
                        .order_by('departure_time')
                )
            ).order_by('bus_number')

            bus_ids = [bus.id for bus in buses]

            # Get last 10 locations for each bus using MySQL-compatible approach
            with connection.cursor() as cursor:
                cursor.execute("""
                       SELECT blh.* FROM (
                           SELECT
                               blh.*,
                               @row_number := IF(@prev_bus = bus_id, @row_number + 1, 1) AS row_num,
                               @prev_bus := bus_id
                           FROM
                               bus_management_buslocationhistory blh,
                               (SELECT @row_number := 0, @prev_bus := 0) AS vars
                           WHERE
                               bus_id IN %s
                           ORDER BY
                               bus_id, timestamp DESC
                       ) AS blh
                       WHERE blh.row_num <= 10
                   """, [tuple(bus_ids) if len(bus_ids) > 1 else (bus_ids[0], bus_ids[0])])

                columns = [col[0] for col in cursor.description]
                location_data = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]

            # Group locations by bus_id
            from collections import defaultdict
            location_map = defaultdict(list)
            for loc in location_data:
                # Convert PointField data if needed
                if 'location' in loc and loc['location']:
                    try:
                        # For MySQL GIS data
                        from django.contrib.gis.geos import GEOSGeometry
                        point = GEOSGeometry(loc['location'])
                        loc['latitude'] = point.y
                        loc['longitude'] = point.x
                    except:
                        # For non-GIS data
                        loc['latitude'] = None
                        loc['longitude'] = None
                location_map[loc['bus_id']].append(loc)

            # Serialize the data
            serialized_data = []
            for bus in buses:
                bus_info = {
                    'id': bus.id,
                    'bus_number': bus.bus_number,
                    'bus_type': bus.get_bus_type_display(),
                    'license_plate': bus.license_plate,
                    'capacity': bus.capacity,
                    'is_active': bus.is_active
                }

                # Driver info
                driver_info = None
                if hasattr(bus, 'driver'):
                    driver = bus.driver
                    driver_info = {
                        'id': driver.id,
                        'name': driver.user.get_full_name(),
                        'license_number': driver.license_number,
                        'experience': driver.years_of_experience
                    }

                # Schedules
                schedules = []
                for schedule in bus.schedules.all():
                    schedules.append({
                        'id': schedule.id,
                        'route_id': schedule.route.id,
                        'route_name': schedule.route.name,
                        'destination': schedule.route.destination,
                        'departure': schedule.departure_time.strftime('%H:%M'),
                        'arrival': schedule.arrival_time.strftime('%H:%M'),
                        'is_active': schedule.is_active
                    })

                # Location history
                locations = []
                for loc in location_map.get(bus.id, []):
                    locations.append({
                        'id': loc['id'],
                        'latitude': loc.get('latitude'),
                        'longitude': loc.get('longitude'),
                        'timestamp': loc['timestamp'].isoformat() if hasattr(loc['timestamp'], 'isoformat') else str(
                            loc['timestamp']),
                        'speed': loc['speed'],
                        'status': loc['status']
                    })

                combined_data = {
                    **bus_info,
                    'driver': driver_info,
                    'schedules': schedules,
                    'locations': locations
                }
                serialized_data.append(combined_data)

            return Response({'buses': serialized_data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f"Failed to fetch bus data: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['get'])
    def single_bus(self, request, pk=None):
        """Get complete data for a single bus"""
        try:
            bus = Bus.objects.select_related('driver', 'driver__user').prefetch_related(
                Prefetch('schedules',
                         queryset=BusSchedule.objects.select_related('route')
                         .order_by('departure_time')),
                Prefetch('location_history',
                         queryset=BusLocationHistory.objects.order_by('-timestamp'))
            ).get(pk=pk)

            # Serialize as in list action
            bus_data = BusSerializer(bus).data

            driver_data = None
            if bus.driver:
                driver_data = {
                    'id': bus.driver.id,
                    'name': bus.driver.user.get_full_name(),
                    'license_number': bus.driver.license_number,
                    'experience_years': bus.driver.years_of_experience
                }

            schedules_data = [{
                'id': schedule.id,
                'route': {
                    'id': schedule.route.id,
                    'name': schedule.route.name,
                    'origin': schedule.route.origin,
                    'destination': schedule.route.destination
                },
                'departure_time': schedule.departure_time.strftime("%H:%M"),
                'arrival_time': schedule.arrival_time.strftime("%H:%M"),
                'is_active': schedule.is_active
            } for schedule in bus.schedules.all()]

            location_history = [{
                'id': loc.id,
                'latitude': loc.location.y if loc.location else None,
                'longitude': loc.location.x if loc.location else None,
                'status': loc.status,
                'timestamp': loc.timestamp,
                'speed': loc.speed
            } for loc in bus.location_history.all()]

            response_data = {
                **bus_data,
                'driver': driver_data,
                'schedules': schedules_data,
                'location_history': location_history
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Bus.DoesNotExist:
            return Response(
                {'error': 'Bus not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = BusSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['bus_type', 'is_active']
    search_fields = ['bus_number', 'license_plate']
    ordering_fields = ['bus_number', 'added_on']


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = DriverSerializer
    filter_backends = [SearchFilter]
    search_fields = ['user__first_name', 'user__last_name', 'license_number']


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'origin', 'destination']


class BusScheduleViewSet(viewsets.ModelViewSet):
    queryset = BusSchedule.objects.all()
    serializer_class = BusScheduleSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['bus', 'route', 'is_active']


class BusLocationViewSet(viewsets.ModelViewSet):
    queryset = BusLocationHistory.objects.all()
    serializer_class = BusLocationSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        bus_id = self.request.query_params.get('bus_id')
        if bus_id:
            queryset = queryset.filter(bus_id=bus_id)
        return queryset.order_by('-timestamp')[:50]
