"""Module for making REST API calls to get information from the database."""

from .auth_api_service import client


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


def create_show_later(myshows_id, title_eng, year):
    """Adding an object to LaterWatchShow model using REST API."""
    data = {"myshows_id": myshows_id, "title_eng": title_eng, "year": year}
    client.session.post(f'{DRF_API_URL}later-watch-shows/', data)


def create_show_full(myshows_id, title_eng, year):
    """Adding an object to LaterWatchShow model using REST API."""
    data = {"myshows_id": myshows_id, "title_eng": title_eng, "year": year}
    client.session.post(f'{DRF_API_URL}full-watched-shows/', data)


def delete_show_later(id):
    """Removing given object from LaterWatchShow model using REST API."""
    client.session.delete(f'{DRF_API_URL}later-watch-shows/{id}')


def delete_show_full(id):
    """Removing given object from FullWatchedShow model using REST API."""
    client.session.delete(f'{DRF_API_URL}full-watched-shows/{id}')


def set_rating(id, rating):
    """Setting a custom rating for a show from FullWatchedShow model using REST API."""
    rating = {"rating": rating}
    client.session.patch(f'{DRF_API_URL}full-watched-shows/{id}/', rating)

