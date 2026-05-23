import os
from celery import Celery

redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

app = Celery("mailmind_workers", broker=redis_url, backend=redis_url)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    imports=['workers.tasks']
)

# Setup periodic task to poll Gmail every 10 seconds
app.conf.beat_schedule = {
    'poll-gmail-every-10-seconds': {
        'task': 'workers.tasks.poll_gmail',
        'schedule': 10.0, # Every 10 seconds
    },
}
