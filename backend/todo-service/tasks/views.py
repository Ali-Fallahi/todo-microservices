from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Read the user ID from the header injected by our API Gateway
        user_id = self.request.headers.get("X-User-ID")
        if not user_id:
            return Todo.objects.none()  # Return empty if no user ID
        return Todo.objects.filter(user_id=user_id)

    def perform_create(self, serializer):
        user_id = self.request.headers.get("X-User-ID")
        # Ensure we have a user_id before saving
        if user_id:
            serializer.save(user_id=user_id)
        else:
            # This case should ideally not be reached if the gateway is working
            raise ValueError("User ID not provided by the gateway")
