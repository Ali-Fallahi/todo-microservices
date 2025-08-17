from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["id", "title", "description", "completed", "created_at", "user_id"]
        read_only_fields = ["user_id"]
        extra_kwargs = {
            "title": {"required": False},
            "description": {"required": False},
        }
