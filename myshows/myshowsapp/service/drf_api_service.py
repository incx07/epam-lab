# pylint: disable=invalid-name,redefined-builtin
"""Module for making REST API calls to get information from the database."""

#from django.contrib.sites.models import Site
from .auth_api_service import client
from .myshows_api_service import myshows_getbyid


#DRF_API_URL = f'{Site.objects.get_current().domain}api/'
DRF_API_URL = 'http://127.0.0.1:8000/api/'


def list_later_watch_show():
    """Getting all objects from LaterWatchShow model using REST API."""
    response = client.session.get(f'{DRF_API_URL}later-watch-shows/')
    shows = sorted(response.json(), key=lambda show: show['title_eng'])
    return shows


def list_full_watched_show():
    """Getting all objects from FullWatchedShow model using REST API."""
    response = client.session.get(f'{DRF_API_URL}full-watched-shows/')
    shows = sorted(response.json(), key=lambda show: show['title_eng'])
    return shows


def create_show_later(myshows_id):
    """
    Adding an object to LaterWatchShow model using REST API.

    ...

    Parameters
    ----------
    myshows_id : int
        id value to search a show in myshows database

    """
    response = myshows_getbyid(myshows_id)
    title_eng = response['result']['titleOriginal']
    year = response['result']['year']
    data = {"myshows_id": myshows_id, "title_eng": title_eng, "year": year}
    client.session.post(f'{DRF_API_URL}later-watch-shows/', data)


def create_show_full(myshows_id):
    """
    Adding an object to FullWatchedShow model using REST API.

    ...

    Parameters
    ----------
    myshows_id : int
        id value to search a show in myshows database

    """
    response = myshows_getbyid(myshows_id)
    title_eng = response['result']['titleOriginal']
    year = response['result']['year']
    data = {"myshows_id": myshows_id, "title_eng": title_eng, "year": year}
    client.session.post(f'{DRF_API_URL}full-watched-shows/', data)


def delete_show_later(id):
    """
    Removing given object from LaterWatchShow model using REST API.

    ...

    Parameters
    ----------
    id : int
        id value to delete a show in DRF database

    """
    client.session.delete(f'{DRF_API_URL}later-watch-shows/{id}')


def delete_show_full(id):
    """
    Removing given object from FullWatchedShow model using REST API.

    ...

    Parameters
    ----------
    id : int
        id value to delete a show in DRF database

    """
    client.session.delete(f'{DRF_API_URL}full-watched-shows/{id}')


def set_rating(id, rating):
    """
    Setting a custom rating for a show from FullWatchedShow model using REST API.

    ...

    Parameters
    ----------
    id : int
        id value to patch a show in DRF database
    rating : int
       rating value from RatingForm

    """
    rating = {"rating": rating}
    client.session.patch(f'{DRF_API_URL}full-watched-shows/{id}/', rating)
