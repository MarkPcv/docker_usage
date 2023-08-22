from django.urls import path
from rest_framework import routers

from habit_tracker.apps import HabitTrackerConfig
from habit_tracker.views import HabitViewSet, HabitPublicListAPIView

app_name = HabitTrackerConfig.name

# Define router for habit viewset
router = routers.DefaultRouter()
router.register('habits', HabitViewSet, basename='habits')

urlpatterns = [
    path('habits/public/', HabitPublicListAPIView.as_view(),
         name='public-list'),
] + router.urls
