from rest_framework import serializers
from .models import Bus, Driver, Route, Schedule, GPSLog, StopTime
from django.utils import timezone

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', 'name', 'start_point', 'end_point', 'stops']

class StopTimeSerializer(serializers.ModelSerializer):
    late_by = serializers.SerializerMethodField()

    class Meta:
        model = StopTime
        fields = [
            'id',
            'stop_name',
            'arrival_time',
            'actual_arrival_time',
            'stop_status',
            'late_by'
        ]
        read_only_fields = ['late_by']

    def get_late_by(self, obj):
        if obj.actual_arrival_time:
            diff = obj.actual_arrival_time - obj.arrival_time
            minutes = int(diff.total_seconds() // 60)
            if minutes > 0:
                return f"{minutes} min late"
            elif minutes < 0:
                return f"{abs(minutes)} min early"
            else:
                return "on time"
        return None

class ScheduleSerializer(serializers.ModelSerializer):
    route = RouteSerializer(read_only=True)
    stop_times = StopTimeSerializer(many=True)  # Allow multiple stop times

    class Meta:
        model = Schedule
        fields = ['id', 'route', 'bus', 'departure_time', 'arrival_time', 'stop_times']

    def create(self, validated_data):
        stop_times_data = validated_data.pop('stop_times')  # Extract stop_times data
        schedule = Schedule.objects.create(**validated_data)  # Create the Schedule instance

        # Create stop times and associate them with the schedule
        for stop_time_data in stop_times_data:
            StopTime.objects.create(schedule=schedule, **stop_time_data)

        return schedule

    def update(self, instance, validated_data):
        stop_times_data = validated_data.pop('stop_times', None)

        # Update base fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if stop_times_data is not None:
            # Delete old stop times
            instance.stop_times.all().delete()

            # Create new stop times
            for stop_time_data in stop_times_data:
                StopTime.objects.create(schedule=instance, **stop_time_data)

        return instance


# class ScheduleSerializer(serializers.ModelSerializer):
#     route = RouteSerializer(read_only=True)
#     stop_times = StopTimeSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Schedule
#         fields = ['id', 'route', 'bus', 'departure_time', 'arrival_time', 'stop_times']
#
#     def create(self, validated_data):
#         stop_times_data = validated_data.pop('stop_times')  # Extract stop_times data
#         schedule = Schedule.objects.create(**validated_data)  # Create the Schedule instance
#
#         # Create stop times and associate them with the schedule
#         for stop_time_data in stop_times_data:
#             StopTime.objects.create(schedule=schedule, **stop_time_data)
#
#         return schedule


class ScheduleWithRouteSerializer(serializers.ModelSerializer):
    route = RouteSerializer(read_only=True)  # Full route details

    class Meta:
        model = Schedule
        fields = ['id', 'route', 'bus', 'departure_time', 'arrival_time']

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'

class BusSerializer(serializers.ModelSerializer):
    last_trip = serializers.SerializerMethodField()
    next_trip = serializers.SerializerMethodField()
    driver = serializers.SerializerMethodField()

    class Meta:
        model = Bus
        fields = '__all__'
        extra_fields = ('last_trip', 'next_trip', 'driver')
        read_only_fields = extra_fields

    def get_last_trip(self, obj):
        last_schedule = Schedule.objects.filter(bus=obj, departure_time__lt=timezone.now()).order_by('-departure_time').first()
        if last_schedule:
            return ScheduleSerializer(last_schedule).data
        return None

    def get_driver(self, obj):
        driver = Driver.objects.filter(assigned_bus=obj).first()
        if driver:
            return DriverSerializer(driver).data
        return None

    def get_next_trip(self, obj):
        next_schedule = Schedule.objects.filter(bus=obj, departure_time__gte=timezone.now()).order_by('departure_time').first()
        if next_schedule:
            return ScheduleSerializer(next_schedule).data
        return None

class GPSLogSerializer(serializers.ModelSerializer):
    bus = BusSerializer()  # Nested bus serializer to include bus info
    timestamp = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")

    class Meta:
        model = GPSLog
        fields = '__all__'
