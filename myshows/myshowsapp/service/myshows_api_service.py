"""Service for searching information in the myshows.me database."""

import requests


MYSHOWS_API_URL = 'https://api.myshows.me/v2/rpc/'


def myshows_search(title):
    """
    Searching for a TV shows by title on the MyShows resource using the API
    based on JSON-RPC 2.0
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
    response = requests.post(MYSHOWS_API_URL, json=rpc).json()
    return response


def myshows_getbyid(myshows_id):
    """
    Getting detail information about a TV show by id on the MyShows resource
    using API based on JSON-RPC 2.0
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
    response = requests.post(MYSHOWS_API_URL, json=rpc).json()
    if 'error' in response:
        return 'not found'
    return response
