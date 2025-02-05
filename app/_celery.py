import datetime

from celery import Celery

from config import settings

from common import setup_logs_dir, LOGS_DIR


celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=['tasks.image_tasks'],
)
celery_app.conf.update(
    task_acks_late=True,
    broker_transport_options={'visibility_timeout': 600, "retry_policy": {"max_retries": 3} },
    task_reject_on_worker_lost=True,
    task_track_started=True,
    task_default_retry_delay=10,
    result_expires=3600,
    broker_connection_retry_on_startup=False
)


if __name__ == '__main__':
    setup_logs_dir(LOGS_DIR)
    LOGFILE = f"{LOGS_DIR}/worker_{datetime.date.today()}%d.log"
    celery_app.start(['worker', "-c" "1",'--loglevel=info', f'--logfile={LOGFILE}'])