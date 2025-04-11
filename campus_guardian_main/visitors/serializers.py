from rest_framework import serializers
from .models import Visitor


class VisitorSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    visitor_type_display = serializers.CharField(source='get_visitor_type_display', read_only=True)

    class Meta:
        model = Visitor
        fields = '__all__'
        read_only_fields = ['check_in', 'check_out', 'host']


# class VisitorCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Visitor
#         field = '__all__'


class VisitorStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = ['status', 'denial_reason']
        extra_kwargs = {
            'denial_reason': {'required': False}
        }