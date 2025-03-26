import os
from django.test import TestCase
from django.conf import settings

class TestProjectStructure(TestCase):
    def test_required_directories_exist(self):
        required_dirs = [
            'media',
            'static',
            'templates',
            'templates/app',
            'static/app',
            'static/app/css',
            'static/app/js',
            'static/app/images'
        ]
        
        for dir_path in required_dirs:
            full_path = os.path.join(settings.BASE_DIR, dir_path)
            self.assertTrue(os.path.exists(full_path), f"Directory {dir_path} does not exist")

    def test_required_files_exist(self):
        required_files = [
            'manage.py',
            'requirements.txt',
            'README.md',
            'Quizzical/settings.py',
            'Quizzical/urls.py',
            'Quizzical/wsgi.py',
            'app/models.py',
            'app/views.py',
            'app/urls.py',
            'templates/app/base.html',
            'templates/app/index.html',
            'static/app/css/style.css',
            'static/app/js/main.js'
        ]
        
        for file_path in required_files:
            full_path = os.path.join(settings.BASE_DIR, file_path)
            self.assertTrue(os.path.exists(full_path), f"File {file_path} does not exist")

    def test_static_files_are_accessible(self):
        static_root = settings.STATIC_ROOT
        self.assertTrue(os.path.exists(static_root), "STATIC_ROOT directory does not exist")
        
        # Check if static files are being collected properly
        self.assertTrue(os.path.exists(os.path.join(static_root, 'app')), 
                       "Static files are not being collected properly")

    def test_media_directory_is_writable(self):
        media_root = settings.MEDIA_ROOT
        self.assertTrue(os.path.exists(media_root), "MEDIA_ROOT directory does not exist")
        self.assertTrue(os.access(media_root, os.W_OK), "MEDIA_ROOT directory is not writable") 