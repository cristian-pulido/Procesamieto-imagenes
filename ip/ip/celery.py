import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ip.settings')

app = Celery('ip')
app.config_from_object('django.conf:settings', namespace='Procesamiento')
app.autodiscover_tasks()
