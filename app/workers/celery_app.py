from celery import Celery
from app.core.config import settings

celery = Celery("sahool", broker=settings.redis_url, backend=settings.redis_url)
celery.conf.task_routes = {
    "app.workers.tasks.fetch_sentinel_image_task": {"queue": "satellite"},
    "app.workers.tasks.compute_ndvi_task": {"queue": "satellite"},
    "app.workers.tasks.change_detection_task": {"queue": "satellite"},
}
