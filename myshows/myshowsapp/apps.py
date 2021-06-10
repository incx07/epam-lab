"""
Module for configuring applications
"""

from django.apps import AppConfig


class MyshowsappConfig(AppConfig):
    """
    Configuring Myshowsapp application
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myshowsapp'
