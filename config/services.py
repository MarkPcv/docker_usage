import requests
from django.conf import settings


def get_bot_url():
    """
    Get bot's invite link
    """
    # Identify API method
    method = '/getMe'
    # Compose URL for request
    url = settings.TELEGRAM_URL + settings.TELEGRAM_API_KEY + method
    # Get bot's information
    response = requests.get(
        url
    )
    return 'https://t.me/' + response.json()['result']['username']
