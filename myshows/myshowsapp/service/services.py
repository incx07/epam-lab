import json
import requests
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .auth import client


def myshows_search(title: str) -> dict:
    """Поиск сериалов по названию на ресурсе MyShows с использованием API
    на базе JSON-RPC 2.0
    """
    rpc = {
            'jsonrpc': '2.0',
            'method': 'shows.Search',
            'params': {
                'query': 'string'
                },
            'id': 1
          }
    rpc['params']['query'] = title
    response = requests.post('https://api.myshows.me/v2/rpc/', json = rpc).json()
    return response


def list_later_watch_show():
    """ Получение всех объектов из LaterWatchShow для пользователя """
    response = client.session.get('http://127.0.0.1:8000/api/later-watch-shows/')
    return response.json()


def list_full_watched_show():
    """ Получение всех объектов из FullWatchedShow для пользователя """
    response = client.session.get('http://127.0.0.1:8000/api/full-watched-shows/')
    return response.json()


class Show():
    id = None
    title_eng = None
    year = None
    show_button_later = True
    show_button_full = True


    def __init__(self, myshows_id):
        self.myshows_id = myshows_id
        self.set_button_later(myshows_id)
        self.set_button_full(myshows_id)


    def myshows_getbyid(self, myshows_id) -> dict:
        """Получение информации о сериале по его id на ресурсе MyShows
        с использованием API на базе JSON-RPC 2.0
        """
        rpc = {
                "jsonrpc": "2.0",
                "method": "shows.GetById",
                "params": {
                    "showId": 0,
                    "withEpisodes": False
                    },
                "id": 1
            }
        rpc['params']['showId'] = myshows_id
        response = requests.post('https://api.myshows.me/v2/rpc/', json = rpc).json()
        self.title_eng = response['result']['titleOriginal']
        self.year = response['result']['year']
        return response


    def set_button_later(self, myshows_id):
        """ Установка флага отображения кнопки "Хочу посмотреть" """
        list_later_watch = list_later_watch_show()
        if isinstance(list_later_watch, list):
            for show in list_later_watch:
                if show["myshows_id"] == myshows_id:
                    self.show_button_later = False
                    self.id = show['id']


    def set_button_full(self, myshows_id):
        """ Установка флага отображения кнопки "Полностью посмотрел" """
        list_full_watched = list_full_watched_show()
        if isinstance(list_full_watched, list):
            for show in list_full_watched:
                if show["myshows_id"] == myshows_id:
                    self.show_button_full = False


    def create_show_later(self):
        """ Добавление объекта в таблицу SerialLater """
        data = {
            "myshows_id": self.myshows_id,
            "title_eng": self.title_eng,
            "year": self.year
        }
        client.session.post('http://127.0.0.1:8000/api/later-watch-shows/', data)


    def create_show_full(self):
        """ Добавление объекта в таблицу SerialComplete и в случае наличия
            данного объекта в таблице SerialLater - удаление оттуда
        """
        data = {
            "myshows_id": self.myshows_id,
            "title_eng": self.title_eng,
            "year": self.year
        }
        client.session.post('http://127.0.0.1:8000/api/full-watched-shows/', data)
        if not self.show_button_later:
            url = 'http://127.0.0.1:8000/api/later-watch-shows/'+ str(self.id)
            print(url)
            client.session.delete(url)



def delete_seriallater(myshows_id, user_id):
    """ Удаление объекта из таблицы SerialLater """
    del_serial = SerialLater.objects.get(
        myshows_id = myshows_id,
        user_link_id = user_id)
    del_serial.delete()

def delete_serialcomplete(myshows_id, user_id):
    """ Удаление объекта из таблицы SerialComplete """
    del_serial = SerialComplete.objects.get(
        myshows_id = myshows_id,
        user_link_id = user_id)
    del_serial.delete()



def set_rating(myshows_id, user_id, rating):
    """ Установка пользовательского рейтинга для сериала в таблице
        SerialComplete
    """
    upd_serial = SerialComplete.objects.get(
        myshows_id=myshows_id,
        user_link_id=user_id)
    upd_serial.rating = rating
    upd_serial.save()


def list_later_watch_show():
    """ Получение всех объектов из LaterWatchShow для пользователя """
    response = client.session.get('http://127.0.0.1:8000/api/later-watch-shows/')
    return response.json()


def list_full_watched_show():
    """ Получение всех объектов из FullWatchedShow для пользователя """
    response = client.session.get('http://127.0.0.1:8000/api/full-watched-shows/')
    return response.json()


def pagination(serials, page):
    """ Стандартная пагинация Django """
    paginator = Paginator(serials, 5)
    try:
        serials_page = paginator.page(page)
    except PageNotAnInteger:
        serials_page = paginator.page(1)
    except EmptyPage:
        serials_page = paginator.page(paginator.num_pages)
    return serials_page
