"""
Model series from the list "Going to watch"
"""

from django.db import models
from django.conf import settings


class ShowToWatch(models.Model):
    """
    Class is containing the description of model fields
    """

    user_link = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    myshows_id = models.PositiveIntegerField(default=0)
    title_eng = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField(default=0)
