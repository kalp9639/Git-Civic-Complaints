# Import the Celery app instance
from .celery import app as celery_app

__all__ = ('celery_app',)