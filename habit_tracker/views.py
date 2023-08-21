from rest_framework import viewsets

from habit_tracker.models import Habit
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
