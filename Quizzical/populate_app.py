import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE',
#                     'tango_with_django_project.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Quizzical.settings')

import django
django.setup()
# from app.models import
def populate():
    pass

if __name__ == '__main__':
    print('Starting Quizzical population script...')
    populate()