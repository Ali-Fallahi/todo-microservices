from rest_framework import serializers
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """

    # Make the password write-only, so it won't be returned in API responses.
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        # Fields to be used for registration.
        fields = ("username", "email", "password")
        extra_kwargs = {"email": {"required": True}}

    def create(self, validated_data):
        """
        Override the create method to handle password hashing.
        """
        # Use the create_user method to ensure the password is properly hashed.
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying user profile information.
    """

    class Meta:
        model = User
        # Fields to be displayed in the profile.
        # We exclude sensitive information like the password.
        fields = ("id", "username", "email")
