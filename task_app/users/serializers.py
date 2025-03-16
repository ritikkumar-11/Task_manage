from rest_framework import serializers
from .models import User  # Import your custom User model

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class for the User model.

    This serializer is used to convert User model instances into JSON representation and vice versa.
    """
    class Meta:
        model = User  # Use your custom User model
        fields = '__all__'  # Include all fields

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User  # Import your custom User model

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User  # Use your custom User model
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, attrs):
        """
        Ensure passwords match.
        """
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        """
        Create a new user instance.
        """
        # Remove 'confirm_password' from validated_data since it's not part of the User model
        validated_data.pop('confirm_password', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user