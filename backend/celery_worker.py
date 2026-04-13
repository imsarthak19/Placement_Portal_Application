from celery import Celery
from celery.schedules import crontab

celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Kolkata',
    enable_utc=True,
    beat_schedule={
        # Monthly Reports - 1st of every month at midnight
        'generate-monthly-reports': {
            'task': 'application.tasks.generate_monthly_placement_reports',
            'schedule': crontab(day_of_month=1, hour=0, minute=0),
        },
        # Interview Reminders - Twice a day (9:00 AM and 6:00 PM)
        'send-daily-reminders': {
            'task': 'application.tasks.send_daily_interview_reminders',
            'schedule': crontab(hour='9,18', minute=0),
        },
    }
)

import application.tasks