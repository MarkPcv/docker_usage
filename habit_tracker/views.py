from rest_framework import viewsets

from habit_tracker.models import Habit
from habit_tracker.permissions import IsOwner
from habit_tracker.serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    """
    CRUD mechanism for model `habit_tracker.Habit` using DRF
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    # authentication_classes = []  #TODO: remove after testing

    def perform_create(self, serializer):
        """Save owner field during creation"""
        new_habit = serializer.save()
        new_habit.owner = self.request.user
        new_habit.save()

    def list(self, request, *args, **kwargs):
        """Override LIST action so that only habits of user are displayed"""
        # Check if user is NOT moderator
        self.queryset = Habit.objects.filter(owner=self.request.user)
        return super().list(request, *args, **kwargs)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that
        this view requires for specific action
        """
        # Define permissions based on view action
        if self.action == 'retrieve':
            # Only Owner can view this habit
            permission_classes = [IsOwner]
        elif self.action == 'update':
            # Only Owner can update this habit
            permission_classes = [IsOwner]
        elif self.action == 'partial_update':
            # Only Owner can partially update this habit
            permission_classes = [IsOwner]
        elif self.action == 'destroy':
            # Only Owner can delete this habit
            permission_classes = [IsOwner]
        else:
            # All users
            permission_classes = []

        return [permission() for permission in permission_classes]
