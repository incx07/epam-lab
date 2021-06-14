"""Module is for a description of a model from the list "Going to watch"."""

from django.db import models
from django.conf import settings


class ShowToWatch(models.Model):
    """
    Class is containing the description of fields for "Going to watch" model.

    ...

    Attributes
    ----------
    user_link : int
        link to the user who added show
    myshows_id : int
        link to id in myshows database
    title_eng : str
        the name of the show
    year : int
        the show release year

    """

    user_link = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    myshows_id = models.PositiveIntegerField(default=0)
    title_eng = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        """Method returns a string representation of object."""
        return str(self.title_eng)
