from rest_framework import generics

from users.serializers import UserSerializer


class CreateUserAPIView(generics.CreateAPIView):
    """
    Create DRF generic for model `users.User`
    """
    serializer_class = UserSerializer
    authentication_classes = []

    def perform_create(self, serializer):
        new_user = serializer.save()
        new_user.set_password(new_user.password)
        new_user.save()
