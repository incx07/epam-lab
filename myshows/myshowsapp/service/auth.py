import requests


class JWTAuth:
    url_create = 'http://127.0.0.1:8000/api/auth/jwt/create/'
    url_refresh = 'http://127.0.0.1:8000/api/auth/jwt/refresh/'
    url_verify = 'http://127.0.0.1:8000/api/auth/jwt/verify/'
    session = requests.Session()
    username = None
    access_token = None
    refresh_token = None
    is_authenticated = False
    error = None


    def login(self, username, password):
        credential = {
            'username': username,
            'password': password
        }
        response = requests.post(self.url_create, json = credential)
        if response.status_code == 200:
            self.refresh_token = response.json()['refresh']
            self.access_token = response.json()['access']
            self.is_authenticated = True
        if response.status_code == 401:
            self.error = response.json()['detail']


    def get_username(self):
        if self.access_token:
            self.session.headers.update({'Authorization': 'JWT ' + self.access_token})
            response = self.session.get('http://127.0.0.1:8000/api/auth/users/me/')
            if response.status_code == 200:
                self.username = response.json()['username']
                return self.username
            else:
                return None


    def verify(self):
        response = requests.post(self.url_verify, json = {'token': self.access_token})
        if response.status_code == 200:
            return True
        if response.status_code == 401:
            return False


    def refresh(self, refresh_token):
        response = requests.post(self.url_refresh, json = {'refresh': refresh_token})
        if response.status_code == 200:
            self.access_token = response.json()['access']
            self.session.headers.update({'Authorization': 'JWT ' + self.access_token})
            self.is_authenticated = True
        if response.status_code == 401:
            self.is_authenticated = False
            self.username = None
            self.session.headers.clear()


client = JWTAuth()


class Registration():
    username = None
    is_registered = False
    errors = None

    def register(self, username, email, password, re_password):
        credential = {
            'username': username,
            'email': email,
            'password': password,
            're_password': re_password
        }
        response = requests.post('http://127.0.0.1:8000/api/auth/users/', json = credential)
        if response.status_code == 201:
            self.is_registered = True
            self.username = response.json()['username']
        if response.status_code == 400:
            for key in response.json():
                self.errors = response.json()[key]


def password_reset_by_email(email):
    requests.post('http://127.0.0.1:8000/api/auth/users/reset_password/', json = {'email': email})


def password_reset_confirmation(uidb64, token, password, re_password):
    credential = {
        'uid': uidb64,
        'token': token,
        'new_password': password,
        're_new_password': re_password
    }
    response = requests.post('http://127.0.0.1:8000/api/auth//users/reset_password_confirm/', json = credential)
    if response.status_code == 204:
        return False
    if response.status_code == 400:
        for key in response.json():
            errors = response.json()[key]
            return errors

