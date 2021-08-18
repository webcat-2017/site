"""
WSGI config for webcatcms project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application
sys.path.append("/var/www/site/")
sys.path.append("/var/www/site/webcatcms/")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcatcms.settings')
application = get_wsgi_application()
