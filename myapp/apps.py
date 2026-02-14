import os
from django.apps import AppConfig
from django.conf import settings

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        # Create media subdirectories on startup
        media_root = settings.MEDIA_ROOT
        subdirs = ['newsniasosi', 'pdfs']  # add any upload_to folders you use
        for sub in subdirs:
            path = os.path.join(media_root, sub)
            os.makedirs(path, exist_ok=True)
