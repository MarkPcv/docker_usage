from rest_framework import routers

from habit_tracker.apps import HabitTrackerConfig
from habit_tracker.views import HabitViewSet

app_name = HabitTrackerConfig.name

# Define router for habit viewset
router = routers.DefaultRouter()
router.register('habits', HabitViewSet, basename='habits')

urlpatterns = [

] + router.urls
