import os
from celery import Celery
from celery.schedules import crontab

redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

app = Celery("mailmind_workers", broker=redis_url, backend=redis_url)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    imports=['backend.workers.tasks']
)

# Setup periodic task to poll Gmail every 5 minutes
app.conf.beat_schedule = {
    'poll-gmail-every-5-minutes': {
        'task': 'backend.workers.tasks.poll_gmail',
        'schedule': crontab(minute='*/5'), # Every 5 minutes
    },
}
