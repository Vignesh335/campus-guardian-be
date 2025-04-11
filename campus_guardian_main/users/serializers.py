from rest_framework import serializers
from django.contrib.auth import get_user_model
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ValidationError

# User = get_user_model()
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # class Meta:
        #     model =
        #     fields = [
        #         'id',
        #         'display_name',
        #         'type',
        #         'department_name',
        #         'is_active',
        #         'staff_id',
        #         'specialization',
        #         'joined_date',
        #         'created_at'
        #     ]
        #     read_only_fields = ['staff_id', 'created_at']

        # model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'user_type', 'phone', 'address', 'profile_picture', 'is_active']
        read_only_fields = ['is_active']
        extra_kwargs = {
            'profile_picture': {'required': False}
        }


# class UserCreateSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, style={'input_type': 'password'})
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'first_name', 'last_name',
#                   'user_type', 'phone', 'address', 'profile_picture']
#         extra_kwargs = {
#             'password': {'write_only': True},
#             'user_type': {'required': True}
#         }
#
#     def validate_user_type(self, value):
#         if value not in dict(User.USER_TYPES).keys():
#             raise ValidationError("Invalid user type")
#         return value
#
#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data.get('email'),
#             password=validated_data['password'],
#             first_name=validated_data.get('first_name', ''),
#             last_name=validated_data.get('last_name', ''),
#             user_type=validated_data['user_type'],
#             phone=validated_data.get('phone'),
#             address=validated_data.get('address')
#         )
#         if 'profile_picture' in validated_data:
#             user.profile_picture = validated_data['profile_picture']
#             user.save()
#         return user
#
#
# class UserUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['email', 'first_name', 'last_name',
#                   'phone', 'address', 'profile_picture']
#         extra_kwargs = {
#             'profile_picture': {'required': False}
#         }
#
#
# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
#         data.update({
#             'id': self.user.id,
#             'username': self.user.username,
#             'email': self.user.email,
#             'user_type': self.user.user_type,
#             'first_name': self.user.first_name,
#             'last_name': self.user.last_name
#         })
#         return data