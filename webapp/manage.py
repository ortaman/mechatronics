#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':

    DJANGO_ENV = os.environ.get('DJANGO_ENV', 'development')

    if DJANGO_ENV == 'production':
        DJANGO_SETTINGS_MODULE = '_mechatronics.settings.production'

    elif DJANGO_ENV == 'development':
        DJANGO_SETTINGS_MODULE = '_mechatronics.settings.development'

    elif DJANGO_ENV == 'staging':
        DJANGO_SETTINGS_MODULE = '_mechatronics.settings.staging'

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', DJANGO_SETTINGS_MODULE)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
