import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object("django.conf:settings", namespace='CELERY')

app.conf.task_routes = {
    'core.tasks.send_sms_task': {'queue':'queue1'},
    'core.tasks.send_sms_for_order_task': {'queue':'queue1'},
}
app.autodiscover_tasks()