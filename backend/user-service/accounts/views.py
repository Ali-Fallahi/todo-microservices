from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegistrationSerializer, UserProfileSerializer


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


class UserProfileView(generics.RetrieveAPIView):
    """
    API view to retrieve the authenticated user's profile.
    """

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Override this method to return the user of the current request.
        """
        return self.request.user
