from rest_framework import serializers
from .models import Bus, Driver, Route, BusSchedule, BusLocationHistory
from ..users.models import User

from ..users.serializers import UserSerializer


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    assigned_bus = serializers.PrimaryKeyRelatedField(queryset=Bus.objects.all(), required=False,
                                                      allow_null=True)

    class Meta:
        model = Driver
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'


class BusScheduleSerializer(serializers.ModelSerializer):
    bus = serializers.PrimaryKeyRelatedField(queryset=Bus.objects.all())
    route = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all(), required=False,
                                                      allow_null=True)
    # bus = BusSerializer()
    # route = RouteSerializer()

    class Meta:
        model = BusSchedule
        fields = '__all__'


class BusLocationSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)

    class Meta:
        model = BusLocationHistory
        fields = ['id', 'bus', 'latitude', 'longitude', 'speed', 'timestamp']
        read_only_fields = ['timestamp']

    def __str__(self):
        return f"{self.bus} at {self.timestamp}"

    # def create(self, validated_data):
    #     latitude = validated_data.pop('latitude')
    #     longitude = validated_data.pop('longitude')
    #     # validated_data['location'] = Point(longitude, latitude)
    #     return super().create(validated_data)