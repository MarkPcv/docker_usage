import requests
from celery import shared_task
from django.conf import settings

from users.models import User


@shared_task
def update_telegram_ids():
    """
    Check current updates of Telegram Bot and update Telegram IDs for users
    """
    # Identify API method
    method = '/getUpdates'
    # Compose URL for request
    url = settings.TELEGRAM_URL + settings.TELEGRAM_API_KEY + method
    # Get Bot updates
    response = requests.get(
        url
    )
    updates = response.json()['result']
    # Search for new email addresses and update Telegram IDs for users
    for update in updates:
        # Check type of message entity
        if update['message']['entities']['type'] == 'email':
            # Get email adressess
            email = update['message']['text']
            # Check if user with this email exists
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                user.telegram_id = update['message']['chat']['id']
    # Confirm updates
    requests.get(
        url,
        params={'offset': updates[-1]['update_id'] + 1}
    )
