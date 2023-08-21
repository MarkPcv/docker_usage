from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habit_tracker.models import Habit
from users.models import User
from django.test import TestCase

# print(response.json()) ## TODO remove after FINISH


class HabitTest(APITestCase):
    """
    Class for testing model `habit_tracker.Model`
    """
    def create_user(self) -> None:
        """Creates a new user for testing"""
        # Create test user with MEMBER role
        self.user = User.objects.create(
            email='test@gmail.com',
            is_active=True,
        )
        self.user.set_password('test')
        self.user.save()

    def setUp(self) -> None:
        """Set up initial objects for each test"""
        # Create MEMBER user
        self.create_user()
        # Create Course object
        self.course = Habit.objects.create(
            place='place1',
            action='action1',
            time='07:00',
            is_pleasant=False,
            is_public=True,
            exec_time=60,
            period=1,
            owner=self.user,
        )

    def test_habit_create(self):
        """Testing habit creation"""
        # Authenticate user without token
        self.client.force_authenticate(self.user)
        # Test data
        data = {
            'place': 'place2',
            'action': 'action2',
            'time': '08:00',
            'is_pleasant': False,
            'is_public': True,
            'exec_time': 100,
            'period': 2
        }
        # Create second habit
        response = self.client.post(
            '/habits/',
            data=data
        )
        # Check status
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        # Check total number of lessons
        self.assertEqual(
            Habit.objects.count(),
            2
        )

    def test_habit_read(self):
        """Testings habit retrieval"""
        # Authenticate user without token
        self.client.force_authenticate(self.user)
        # Get first habit
        response = self.client.get(
            '/habits/1/'
        )
        # Check status
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        # Check habit data
        self.assertEqual(
            response.json(),
            {'id': 1, 'place': 'place1', 'action': 'action1',
             'time': '07:00:00', 'is_pleasant': False, 'is_public': True,
             'exec_time': 60, 'period': 1, 'award': None,
             'associated_habit': None, 'owner': 1}
        )



