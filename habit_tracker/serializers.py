from rest_framework import serializers

from habit_tracker.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """
    Serializer for model `habit_tracker.Habit`
    """

    class Meta:
        model = Habit
        fields = '__all__'
