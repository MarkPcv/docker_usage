from django.db import models

from users.models import User, NULLABLE


class Habit(models.Model):
    """
    Stores a single habit entry.
    """
    # Main fields
    place = models.TextField(verbose_name='place')
    action = models.TextField(verbose_name='action')
    time = models.TimeField(verbose_name='time')
    # Behaviour fields
    is_pleasant = models.BooleanField(verbose_name='is_pleasant')
    is_public = models.BooleanField(verbose_name='is_public')
    # Habit settings
    exec_time = models.PositiveIntegerField(verbose_name='exec_time')
    period = models.PositiveIntegerField(default=1, verbose_name='period')
    # Relations and awards
    award = models.TextField(verbose_name='award', **NULLABLE)
    associated_habit = models.ForeignKey("Habit", on_delete=models.SET_NULL,
                                         **NULLABLE,
                                         verbose_name='related_habit')
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              verbose_name='owner', **NULLABLE)

    def __str__(self):
        return f'I will {self.action} at {self.time} in {self.place}'

    class Meta:
        verbose_name = 'habit'
        verbose_name_plural = 'habits'
        ordering = ('owner',)

