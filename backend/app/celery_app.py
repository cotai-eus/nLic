from celery import Celery
from app.core.config import settings

celery_app = Celery("nradar", broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)

celery_app.conf.update(task_track_started=True)

# Import tasks so Celery can discover them
from app.workers import radar_worker

# Schedule tasks
celery_app.conf.beat_schedule = {
    'monitor-opportunities-every-30-minutes': {
        'task': 'app.workers.radar_worker.monitor_opportunities',
        'schedule': 28800.0,  # 8 hours in seconds
    },
}

app = celery_app # Explicitly define 'app' for Celery discovery
