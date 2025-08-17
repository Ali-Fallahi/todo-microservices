from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from kafka import KafkaProducer
import json


class UserRegistrationView(generics.CreateAPIView):
    """
    API view for user registration.
    """

    serializer_class = UserRegistrationSerializer
    # Allow any user (authenticated or not) to access this endpoint.
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            # You can customize the response data here if you want.
            # For example, returning a success message.
            return Response(
                {
                    "user": {"username": user.username, "email": user.email},
                    "message": "User created successfully.",
                },
                status=status.HTTP_201_CREATED,
            )
        # The raise_exception=True in is_valid will handle the error case,
        # so we don't strictly need to return a 400 response here.


class UserProfileView(generics.RetrieveDestroyAPIView):  # Changed to allow DELETE
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        user_id = instance.id

        # Call the parent class method to delete the user from the database
        super().perform_destroy(instance)

        # After successful deletion, send a message to Kafka
        try:
            producer = KafkaProducer(
                bootstrap_servers="kafka:9092",
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
            producer.send("user_deleted_topic", {"user_id": user_id})
            producer.flush()  # Ensure the message is sent
            print(f"Sent user_deleted event for user_id: {user_id}")
        except Exception as e:
            # In a real app, you'd have more robust error handling/logging
            print(f"Error sending to Kafka: {e}")
