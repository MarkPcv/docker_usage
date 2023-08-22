from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTest(APITestCase):
    """
    Class for testing model `habit_tracker.Model`
    """
    def setUp(self) -> None:
        pass

    def test_user_create(self):
        """
        Testing user registration
        """
        # Test data
        data = {
            'email': 'test@gmail.com',
            'password': 'test'
        }
        # Register user
        response = self.client.post(
            '/users/register/',
            data=data
        )
        # Check status
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        # Check email of registered user
        self.assertEqual(
            User.objects.all()[0].email,
            'test@gmail.com'
        )

    def test_createsuperuser_command(self):
        """
        Testings custom management command for superuser creation
        """
        # Call custom command
        call_command('csu')
        # Get user
        user = User.objects.all()[0]
        # Check email of newly created superuser
        self.assertEqual(
            user.email,
            'admin@gmail.com'
        )
        # Check admin property of user
        self.assertTrue(
            user.is_superuser
        )
