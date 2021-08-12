from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .auth_api_service import client
from .myshows_api_service import myshows_getbyid


def list_later_watch_show():
    """ Получение всех объектов из LaterWatchShow для пользователя """
    response = client.session.get('http://127.0.0.1:8000/api/later-watch-shows/')
    shows = sorted(response.json(), key=lambda show: show['title_eng'])
    return shows


def list_full_watched_show():
    """ Получение всех объектов из FullWatchedShow для пользователя """
    response = client.session.get('http://127.0.0.1:8000/api/full-watched-shows/')
    shows = sorted(response.json(), key=lambda show: show['title_eng'])
    return shows


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


    def get_by_id(self, myshows_id):
        response = myshows_getbyid(myshows_id)
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
            client.session.delete(url)



def delete_show_later(id):
    """ Удаление объекта из таблицы SerialLater """
    url = 'http://127.0.0.1:8000/api/later-watch-shows/'+ str(id)
    client.session.delete(url)


def delete_show_full(id):
    """ Удаление объекта из таблицы SerialComplete """
    url = 'http://127.0.0.1:8000/api/full-watched-shows/'+ str(id)
    client.session.delete(url)


def set_rating(id, rating):
    """ Установка пользовательского рейтинга для сериала в таблице
        SerialComplete
    """
    url = 'http://127.0.0.1:8000/api/full-watched-shows/'+ str(id) + '/'
    rating = {"rating": rating} 
    client.session.patch(url, rating)


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