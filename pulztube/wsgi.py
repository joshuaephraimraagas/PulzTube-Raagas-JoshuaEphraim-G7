"""
WSGI config for pulztube project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulztube.settings')

application = get_wsgi_application()
