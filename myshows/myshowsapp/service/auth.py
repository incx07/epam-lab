import requests


class JWTAuth:
    url_create = 'http://127.0.0.1:8000/api/auth/jwt/create/'
    url_refresh = 'http://127.0.0.1:8000/api/auth/jwt/refresh/'
    url_verify = 'http://127.0.0.1:8000/api/auth/jwt/verify/'
    username = None
    access_token = None
    refresh_token = None
    is_authenticated = False
    error = None


    def login(self, usernamevalue, passwordvalue):
        print(10)
        credential = {
            'username': usernamevalue,
            'password': passwordvalue
        }
        print(11)
        response = requests.post(self.url_create, json = credential)
        print(response)
        if response.status_code == 200:
            self.refresh_token = response.json()['refresh']
            self.access_token = response.json()['access']
            self.is_authenticated = True
        if response.status_code == 401:
            self.error = response.json()['detail']


    def get_username(self):
        response = requests.get(
            'http://127.0.0.1:8000/api/auth/users/me/',
            headers={'Authorization': 'JWT ' + self.access_token}
        )
        self.username = response.json()['username']
        return self.username


    def verify(self):
        response = requests.post(self.url_verify, json = {'token': self.access_token})
        if response.status_code == 200:
            return True
        if response.status_code == 401:
            return False


    def resresh(self):
        response = requests.post(self.url_refresh, json = {'refresh': self.refresh_token})
        if response.status_code == 200:
            self.access_token = response.json()['access']
        if response.status_code == 401:
            self.is_authenticated = False
            self.username = None
            error = 'User is not authenticated'
            return error


client = JWTAuth()
