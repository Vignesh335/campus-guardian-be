from rest_framework import serializers
from .models import Lecturer, Attendance
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
            'created_at',
            'email'
        ]
        read_only_fields = ['staff_id', 'created_at']

    def validate_department_name(self, value):
        if len(value) < 2:
            raise ValidationError("Department name must be at least 2 characters long.")
        return value

class AttendanceSerializer(serializers.ModelSerializer):
    lecturer = LecturerSerializer(read_only=True)
    lecturer_id = serializers.PrimaryKeyRelatedField(
        queryset=Lecturer.objects.all(), source='lecturer', write_only=True
    )

    class Meta:
        model = Attendance
        fields = ['id', 'lecturer', 'lecturer_id', 'date', 'status', 'remarks', 'recorded_at']

# class WebAuthnRegistrationSerializer(serializers.Serializer):
#     credential_id = serializers.CharField()
#     public_key = serializers.CharField()
#     lecturer_id = serializers.IntegerField()
#
#     def create(self, validated_data):
#         lecturer = Lecturer.objects.get(id=validated_data['lecturer_id'])
#         return WebAuthnCredential.objects.create(
#             lecturer=lecturer,
#             credential_id=validated_data['credential_id'],
#             public_key=validated_data['public_key']
#         )