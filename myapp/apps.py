import os
from django.apps import AppConfig
from django.conf import settings

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        # Create necessary media subdirectories on application startup
        media_root = settings.MEDIA_ROOT
        # Add both 'pdfs' and 'newsniasosi' to the list
        subdirs_to_create = ['pdfs', 'newsniasosi']
        for subdir in subdirs_to_create:
            dir_path = os.path.join(media_root, subdir)
            try:
                os.makedirs(dir_path, exist_ok=True)
                print(f"Ensured directory exists: {dir_path}")
            except Exception as e:
                print(f"Error creating directory {dir_path}: {e}")
