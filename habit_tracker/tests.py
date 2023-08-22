import datetime

from rest_framework import status
from rest_framework.test import APITestCase

from habit_tracker.models import Habit
from users.models import User


class HabitTest(APITestCase):
    """
    Class for testing model `habit_tracker.Model`
    """

    def create_user(self):
        """Creates a new user for testing"""
        # Create test user with MEMBER role
        self.user = User.objects.create(
            email='test@gmail.com',
            is_active=True,
        )
        self.user.set_password('test')
        self.user.save()

    def setUp(self):
        """Set up initial objects for each test"""
        # Create MEMBER user
        self.create_user()
        # Create Course object
        self.habit = Habit.objects.create(
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
        # Check total number of habits
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
            f'/habits/{self.habit.pk}/'
        )
        # Check status
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        # Check habit data
        self.assertEqual(
            response.json(),
            {'id': self.habit.pk, 'place': 'place1', 'action': 'action1',
             'time': '07:00:00', 'is_pleasant': False, 'is_public': True,
             'exec_time': 60, 'period': 1, 'award': None,
             'created_on': datetime.date.today().__str__(),
             'associated_habit': None, 'owner': self.user.pk}
        )

    def test_habit_partial_update(self):
        """Testing habit partial update"""
        # Authenticate user without token
        self.client.force_authenticate(self.user)
        # Update action of habit
        data = {
            'action': 'new action'
        }
        # Change first habit
        response = self.client.patch(
            f'/habits/{self.habit.pk}/',
            data=data
        )
        # Check status
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        # Check action change
        self.assertEqual(
            Habit.objects.get(pk=self.habit.pk).action,
            'new action'
        )

    def test_habit_update(self):
        """Testing habit full update"""
        # Authenticate user without token
        self.client.force_authenticate(self.user)

        # Test data
        data = {
            'place': 'place2',
            'action': 'action2',
            'time': '07:00',
            'is_pleasant': False,
            'is_public': True,
            'exec_time': 60,
            'period': 1
        }
        # Create second habit
        response = self.client.put(
            f'/habits/{self.habit.pk}/',
            data=data
        )

        # Check status
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        # Check habit data
        new_habit = Habit.objects.all()[0]
        self.assertEqual(
            {'place': new_habit.place, 'action': new_habit.action},
            {'place': 'place2', 'action': 'action2'}
        )

    def test_habit_delete(self):
        """Testing habit deletion"""
        # Authenticate user without token
        self.client.force_authenticate(self.user)
        # Delete first habit
        response = self.client.delete(
            f'/habits/{self.habit.pk}/'
        )
        # Check status
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        # Check that no habit exists in Database
        self.assertFalse(
            Habit.objects.exists()
        )

    def test_habit_list(self):
        """Testing list of habits"""
        # Authenticate user without token
        self.client.force_authenticate(self.user)
        # Get the list of habits
        response = self.client.get(
            '/habits/'
        )
        # Check status
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        # Check habit data
        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [{'id': self.habit.pk, 'place': 'place1',
                             'action': 'action1',
                             'time': '07:00:00', 'is_pleasant': False,
                             'is_public': True,
                             'exec_time': 60, 'period': 1, 'award': None,
                             'created_on': datetime.date.today().__str__(),
                             'associated_habit': None, 'owner': self.user.pk}]
            }
        )

    def test_habit_print(self):
        """Testing string representation of habit model"""
        self.assertEqual(
            self.habit.__str__(),
            'I will action1 at 07:00 in place1'
        )

    def test_validate_period_exceeds(self):
        """Testing period validation case when it is greater than 7 days"""
        # Authenticate user without token
        self.client.force_authenticate(self.user)
        # Update action of habit
        data = {
            'period': 10
        }
        # Change period habit
        response = self.client.patch(
            f'/habits/{self.habit.pk}/',
            data=data
        )
        # Check validation case
        self.assertEqual(
            response.json(),
            {
                "period": [
                    "The period must be less or equal than 7 days"
                ]
            }
        )

    def test_validate_period_zero(self):
        """Testing period validation when it is a zero"""
        # Authenticate user without token
        self.client.force_authenticate(self.user)
        # Update period of habit
        data = {
            'period': 0
        }
        # Change first habit
        response = self.client.patch(
            f'/habits/{self.habit.pk}/',
            data=data
        )
        # Check validation case
        self.assertEqual(
            response.json(),
            {
                "period": [
                    "The period must be a non zero number"
                ]
            }
        )

    def test_validate_exec_time_exceeds(self):
        """
        Testing execution time validation case when it exceeds 120 seconds
        """
        # Authenticate user without token
        self.client.force_authenticate(self.user)
        # Update execution time of habit
        data = {
            'exec_time': 200
        }
        # Change first habit
        response = self.client.patch(
            f'/habits/{self.habit.pk}/',
            data=data
        )
        # Check validation case
        self.assertEqual(
            response.json(),
            {
                "exec_time": [
                    "The execution time cannot exceed 120 seconds"
                ]
            }
        )

    def test_validate_exec_time_zero(self):
        """
        Testing execution time validation case when it is a zero
        """
        # Authenticate user without token
        self.client.force_authenticate(self.user)
        # Update execution time of habit
        data = {
            'exec_time': 0
        }
        # Change first habit
        response = self.client.patch(
            f'/habits/{self.habit.pk}/',
            data=data
        )
        # Check validation case
        self.assertEqual(
            response.json(),
            {
                "exec_time": [
                    "The execution time must be a non zero number"
                ]
            }
        )

    def test_validate_associated_habit(self):
        """
        Testing validation case when associated habit cannot be pleasant
        """
        # Authenticate user without token
        self.client.force_authenticate(self.user)
        # Create second habit
        response = self.client.post(
            '/habits/',
            data={
                'place': 'place2',
                'action': 'action2',
                'time': '08:00',
                'is_pleasant': False,
                'is_public': True,
                'exec_time': 100,
                'period': 2
            }
        )
        # Add second habit to first as associated
        response = self.client.patch(
            f'/habits/{self.habit.pk}/',
            data={
                'associated_habit': response.json()['id']
            }
        )
        # Check validation case
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "The associated habit must be pleasant"
                ]
            }
        )

    def test_validate_habit_has_both(self):
        """
        Testing validation case when habit has both award and associated
        habit
        """
        # Authenticate user without token
        self.client.force_authenticate(self.user)
        # Create second habit
        response = self.client.post(
            '/habits/',
            data={
                'place': 'place2',
                'action': 'action2',
                'time': '08:00',
                'is_pleasant': True,
                'is_public': True,
                'exec_time': 100,
                'period': 2
            }
        )
        # Add second habit to first as associated
        response = self.client.patch(
            f'/habits/{self.habit.pk}/',
            data={
                'associated_habit': response.json()['id'],
                'award': 'do something'
            }
        )
        # Check validation case
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "Habit cannot have both associated habit and award"
                ]
            }
        )

    def test_validate_pleasant_habit(self):
        """
        Testing validation case when pleasant habit has either award or
        associated habit
        """
        # Authenticate user without token
        self.client.force_authenticate(self.user)
        # Create second habit
        response = self.client.post(
            '/habits/',
            data={
                'place': 'place2',
                'action': 'action2',
                'time': '08:00',
                'is_pleasant': True,
                'is_public': True,
                'exec_time': 100,
                'period': 2
            }
        )
        # Get second habit id
        habit_id = response.json()['id']
        # Modify first habit
        self.client.patch(
            f'/habits/{self.habit.pk}/',
            data={
                'is_pleasant': True
            }
        )
        # Add first habit to second as associated
        response = self.client.patch(
            f'/habits/{habit_id}/',
            data={
                'associated_habit': self.habit.pk,
            }
        )
        # Check validation case - pleasant habit has associated habit
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "The pleasant habit cannot have associated habit"
                ]
            }
        )
        # Add award to first pleasant habit
        response = self.client.patch(
            f'/habits/{self.habit.pk}/',
            data={
                'award': 'do_something'
            }
        )
        # Check validation case - pleasant habit has award
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "The pleasant habit cannot have award"
                ]
            }
        )
