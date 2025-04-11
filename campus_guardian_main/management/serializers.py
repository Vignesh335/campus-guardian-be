from rest_framework import serializers
from .models import Lecturer
from django.core.exceptions import ValidationError

class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = [
            'id',
            'display_name',
            'type',
            'department_name',
            'is_active',
            'staff_id',
            'specialization',
            'joined_date',
            'created_at'
        ]
        read_only_fields = ['staff_id', 'created_at']

    def validate_department_name(self, value):
        if len(value) < 2:
            raise ValidationError("Department name must be at least 2 characters long.")
        return value