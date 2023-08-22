import datetime

import requests
from celery import shared_task
from django.conf import settings

from habit_tracker.models import Habit
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
        if update['message']['entities'][0]['type'] == 'email':
            # Get email adressess
            email = update['message']['text']
            # Check if user with this email exists
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                user.telegram_id = update['message']['chat']['id']
                user.save()
    # Confirm updates
    if updates:
        requests.get(
            url,
            params={'offset': updates[-1]['update_id'] + 1}
        )


@shared_task
def send_notifications():
    """
    Sends notification about habit for today to each user with Telegram ID
    """
    # Identify API method
    method = '/sendMessage'
    # Compose URL for request
    url = settings.TELEGRAM_URL + settings.TELEGRAM_API_KEY + method
    # Send message to all users at 1am
    for user in User.objects.all():
        # Skip iteration if user still does not have Telegram ID established
        if not user.telegram_id:
            continue
        # Create message for telegram bot
        message = f"Hi there\!\nHere are your habits for today:\n\n"
        # Identify the list of habits to be done today
        habits = Habit.objects.filter(owner=user).order_by('time')
        # Check each habit and add to message
        for habit in habits:
            # Find difference between creation date and today's date
            diff = datetime.date.today() - habit.created_on
            # Check if habit should be done today
            if diff.days // habit.period != 0:
                continue
            # Pleasant habits are not added to notification message
            elif not habit.is_pleasant:
                # Update message for a single habit
                message += (
                    f"*{habit.time.strftime('%H:%M')}*"
                    f" \- {habit.action.upper()} in {habit.place}\n\n"
                )
        # Identify parameters
        params = {
            'chat_id': user.telegram_id,
            'text': message,
            'parse_mode': 'MarkdownV2'
        }
        # Send notification
        requests.post(
            url,
            params=params,
        )
