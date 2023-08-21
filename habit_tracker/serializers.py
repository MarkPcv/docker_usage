from rest_framework import serializers

from habit_tracker.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """
    Serializer for model `habit_tracker.Habit`
    """

    class Meta:
        model = Habit
        fields = '__all__'

    def validate_period(self, value):
        """
        Validates period of habit
        """
        # Check if period is too rare
        if value > 7:
            raise serializers.ValidationError(
                "The period must be less or equal than 7 days")
        # Check if period exists
        if value == 0:
            raise serializers.ValidationError(
                "The period must be a non zero number")
        return value

    def validate_exec_time(self, value):
        """
        Validates execution time of habit
        """
        # Check if execution time is too long
        if value > 120:
            raise serializers.ValidationError(
                "The execution time cannot exceed 120 seconds")
        # Check if execution time exists
        if value == 0:
            raise serializers.ValidationError(
                "The execution time must be a non zero number")
        return value

    def validate(self, data):
        """
        Validates the specific situations
        """
        # Requirement 1:
        # Only pleasant habit can be used as associated habit
        if data.get('associated_habit', None):
            ass_habit = data['associated_habit']
            if not ass_habit.is_pleasant:
                raise serializers.ValidationError(
                    "The associated habit must be pleasant")
        # Requirement 2:
        # Habit cannot have both associated habit and award
        # Check that existence of both fields in the object
        ass_habit = data.get('associated_habit',
                             self.instance.associated_habit)
        award = data.get('award',
                         self.instance.award)
        if ass_habit and award:
            raise serializers.ValidationError(
                "Habit cannot have both associated habit and award")



        return data
