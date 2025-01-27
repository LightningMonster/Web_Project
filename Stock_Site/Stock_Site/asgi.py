"""
ASGI config for Stock_Site project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application # Function to create the ASGI application callable

# Setting the default settings module for the Django project
# This tells Django which settings file to use (e.g., 'Stock_Site/settings.py').
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Stock_Site.settings')

# Creating the ASGI application callable
# The ASGI server (like Daphne or Uvicorn) uses this callable to communicate with Django.
# initializes Django and prepares it to handle incoming requests.
# The `application` object is the main entry point that the ASGI server will use to forward requests to Django.
application = get_asgi_application()
