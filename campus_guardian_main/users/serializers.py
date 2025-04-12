from rest_framework import serializers
from .models import User, Login

class UserWithLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'full_name',
            'user_type',
            'phone',
            'email',
            'address',
            'is_active',
            'profile_picture',
            'username',
            'password',
        ]
        read_only_fields = ['id', 'full_name']

    def get_full_name(self, obj):
        return obj.get_full_name()

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value

    def validate_username(self, value):
        if Login.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("Username is already taken.")
        return value

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email = validated_data.get('email')

        user = User.objects.create(**validated_data)

        login = Login(user=user, username=username)
        login.set_password(password)
        login.save()

        return user

    def update(self, instance, validated_data):
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', None)

        # Update user instance fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update related login model
        if hasattr(instance, 'login'):
            login = instance.login

            # Username uniqueness check, excluding the current login ID
            if username:
                if Login.objects.exclude(id=login.id).filter(username__iexact=username).exists():
                    raise serializers.ValidationError({"username": "Username is already taken."})
                login.username = username

            # Set new password if provided
            if password:
                login.set_password(password)

            login.save()

        return instance
