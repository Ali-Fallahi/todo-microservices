from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["id", "title", "description", "completed", "created_at", "user_id"]
        # Make user_id read-only because it should be set automatically
        # based on the authenticated user, not sent by the client.
        read_only_fields = ["user_id"]
