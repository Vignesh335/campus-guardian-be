from rest_framework import serializers
from .models import VoiceText, Feedback, Reply
from ..users.models import User
from ..users.serializers import UserWithLoginSerializer


class VoiceTextSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    user_data = serializers.SerializerMethodField()  # Custom field for serialized user data

    class Meta:
        model = VoiceText
        fields = ['id', 'user', 'user_data', 'title', 'audio_file', 'transcription', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_user_data(self, obj):
        # Pass the request context when instantiating UserSerializer
        user = obj.user
        return UserWithLoginSerializer(user, context=self.context).data  # Ensure context is passed

    def create(self, validated_data):
        # If the user is not part of the validated data, take it from the request context
        user = validated_data.get('user', self.context['request'].user)
        validated_data['user'] = user
        return super().create(validated_data)


class ReplySerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    user = serializers.SerializerMethodField()
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    # user_data = serializers.SerializerMethodField()

    # def get_user_data(self, obj):
    #     user = obj.user
    #     return UserSerializer(user, context=self.context).data  # Ensure context is passed
    def get_user(self, obj):
        user = obj.user
        return UserWithLoginSerializer(user, context=self.context).data  # Ensure context is passed

    class Meta:
        model = Reply
        fields = ['id', 'feedback', 'user_id', 'user', 'reply_text', 'created_at', 'user']
        read_only_fields = ['id', 'created_at']

    def validate_user_id(self, value):
        """Validate if the user_id exists in the database."""
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User with the given ID does not exist.")
        return value

    def create(self, validated_data):
        # Extract user_id from validated_data and assign the user instance
        user_id = validated_data.pop('user_id')
        user = User.objects.get(id=user_id)
        validated_data['user'] = user

        return super().create(validated_data)


class FeedbackSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    user = serializers.SerializerMethodField()
    replies = ReplySerializer(many=True, read_only=True)

    category = serializers.ChoiceField(choices=Feedback.CATEGORY_CHOICES)
    feedback_text = serializers.CharField(max_length=500)

    class Meta:
        model = Feedback
        fields = ['id', 'user', 'user_id', 'category', 'feedback_text', 'created_at', 'replies']
        read_only_fields = ['id', 'created_at']

    def get_user(self, obj):
        user = obj.user
        print(user)
        return UserWithLoginSerializer(user, context=self.context).data  # Ensure context is passed

    def validate_user_id(self, value):
        """Validate if the user_id exists in the database."""
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User with the given ID does not exist.")
        return value

    def create(self, validated_data):
        # Extract user_id from validated_data and assign the user instance
        user_id = validated_data.pop('user_id')
        user = User.objects.get(id=user_id)
        validated_data['user'] = user

        return super().create(validated_data)

