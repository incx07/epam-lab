import requests


def myshows_search(title):
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


def myshows_getbyid(myshows_id):
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
    response = requests.post('https://api.myshows.me/v2/rpc/', json=rpc).json()
    return response
