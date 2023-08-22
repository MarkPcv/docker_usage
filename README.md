# Project «Tracker of Good Habits»

## Description

This project was inspired by the book "Atomic Habits" written by James Clear.
The main idea of the book is to obtain good habits and removing bad ones
through system. The Tracker webapp is realised via Django REST Framework. The
CORS has been set for the project and API documentation is available.

The service provides certain actions to user:

- To register
- To authorize through JWT token
- To create, modify and delete a habit
- To view list of his own habits
- To view list of public habits (includes habits of other users)

After registration an invitation link will be included in server response (JSON
format) back to user. By using it user can connect to Telegram Bot, which will
notify user every day at 1 am (Moscow Time) about habits he has to complete.
Notification tasks are executed using Celery.

---

### Habit Constraints

There are several constraints during habit creation and modification:

1. Period or frequency - how often a habit should occur. The period should not
   exceed 7 days
2. Execution time of habit should not exceed 120 seconds
3. User is allowed to create a pleasant habit. This type of habit is result of
   completing another habit. This habit should not have any award or associated
   habit.
4. Habit can have an award or associated habit but not **both**.
5. Only pleasant habit can be used as associated.

---

### Telegram Integration

As mentioned previously, user can **start** conversation with Telegram Bot (named HabitTrackerBot) via invitation link. This link can only be obtained
during registration from JSON object of the response. When chat with Telegram
Bot is established user should send its email to Telegram Bot.

After completing above steps user will receive notification about habits for
the day in the next early morning. Keep in mind that notifications do not
mention pleasant habits.
---

### Authorization

In order to utilise API methods user should pass authorization token for each
HTTP request method (except registration). The token can be generated and
obtained via link below:

```bash
http://<server_url>/users/token/
```

---

### Documentation

Two types of API documentation can be accessed via following links:

```bash
http://<server_url>/redoc/ 
```

or

```bash
http://<server_url>/docs/
```

---

### Administration

The service has admin access which can be enabled by running the command below:

```bash
python3 manage.py csu
```

If different admin credentials are needed, modify the csu.py located as:

```bash
.
└── users
    └── management
        └── commands
            └── csu.py
```

---

## Installation and Run

Activate environment and use the package manager **poetry** to install all
necessary packages:

```bash
poetry shell
poetry install
```

To establish project settings, create <code>.env</code> file in the project
root directory and fill it. Example is illustrated
in <code>.env.sample</code> file.

Create database and make migrations:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

Run Django server:

```bash
python3 manage.py runserver
```

Run Celery worker and beat:

```bash
celery -A config worker -l INFO
celery -A config beat -l INFO 
```

---

## Tech Stack

<img src="https://img.shields.io/badge/rest-blue?style=for-the-badge&logo=REST&logoColor=white" />
<img src="https://img.shields.io/badge/Django-blue?style=for-the-badge&logo=django&logoColor=white" />
<img src="https://img.shields.io/badge/celery-blue?style=for-the-badge&logo=celery&logoColor=white" />
<img src="https://img.shields.io/badge/Python-blue?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/postgresql-blue?style=for-the-badge&logo=postgresql&logoColor=white" />
<img src="https://img.shields.io/badge/GIT-blue?style=for-the-badge&logo=git&logoColor=white" />
<img src="https://img.shields.io/badge/Poetry-blue?style=for-the-badge&logo=poetry&logoColor=white" />
