import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsdigest.settings')

app = Celery('newsdigest')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks() 