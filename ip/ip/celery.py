import os
from celery import Celery
from celery._state import _set_current_app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ip.settings')

app = Celery('ip',broker='amqp://col2:col2@localhost:5672/image')
app.config_from_object('django.conf:settings', namespace='ip')
_set_current_app(app)
app.autodiscover_tasks()
