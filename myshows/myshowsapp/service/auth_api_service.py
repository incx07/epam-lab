"""Module for making REST API calls for user authentication."""

import requests
#from django.contrib.sites.models import Site


#AUTH_API_URL = f'{Site.objects.get_current().domain}api/auth/'
AUTH_API_URL = 'http://127.0.0.1:8000/api/auth/'


class JWTAuth:
    """
    Class for managing the current user's status in the application.

    ...

    Attributes
    ----------
    url_create : str
        the endpoint to obtain JWT
    url_refresh : str
        the endpoint to refresh JWT
    session : requests.Session object
        used when a request needs to be send with an access token in the headers
    is_authenticated : False or True
        the status of current user (passed to context)
    username : str or None
        the name of current user (passed to context)
    access_token : str or None
        JSON Web Token for access
    refresh_token : str or None
        JSON Web Token for update access token
    error : str or None
        the error message when login was unsuccessful

    """

    url_create = f'{AUTH_API_URL}jwt/create/'
    url_refresh = f'{AUTH_API_URL}jwt/refresh/'
    session = requests.Session()
    is_authenticated = False
    username = None
    access_token = None
    refresh_token = None
    error = None

    def login(self, username, password):
        """
        Used to authorize a user.
        If response contains the status 'HTTP_200_OK', access and refresh tokens
        will be received and saved.
        access and refresh tokens.
        If response contains the status 'HTTP_401_UNAUTHORIZED', we receive
        and save the error message.

        ...

        Parameters
        ----------
        username : str
            username value from LoginForm
        password : str
            password value from LoginForm

        """

        credential = {
            'username': username,
            'password': password
        }
        response = requests.post(self.url_create, json=credential)
        if response.status_code == 200:
            self.refresh_token = response.json()['refresh']
            self.access_token = response.json()['access']
            self.is_authenticated = True
        if response.status_code == 401:
            self.error = response.json()['detail']

    def get_username(self):
        """
        Retrieve/update the authenticated user.
        Executed only for authenticated user (when the access token is not None)
        If response contains the status 'HTTP_200_OK', we receive and save
        the name of current user.

        """
        if self.access_token:
            self.session.headers.update({'Authorization': 'JWT ' + self.access_token})
            response = self.session.get(f'{AUTH_API_URL}users/me/')
            if response.status_code == 200:
                self.username = response.json()['username']
                return self.username
            return None
        return None

    def refresh(self, refresh_token):
        """
        Used to to refresh JWT.
        If response contains the status 'HTTP_200_OK', new access token
        will be received and saved in the headers of requests.Session.
        If response contains the status 'HTTP_401_UNAUTHORIZED', headers
        will be cleared.

        ...

        Parameters
        ----------
        refresh_token : str
            JSON Web Token for update access token

        """
        response = requests.post(self.url_refresh, json={'refresh': refresh_token})
        if response.status_code == 200:
            self.access_token = response.json()['access']
            self.session.headers.update({'Authorization': 'JWT ' + self.access_token})
            self.is_authenticated = True
        if response.status_code == 401:
            self.is_authenticated = False
            self.username = None
            self.session.headers.clear()


client = JWTAuth()


def register(username, email, password, re_password):
    """
    Used to register new user.
    If response contains the status 'HTTP_201_CREATED', the function returns
    username. If response contains the status 'HTTP_400_BAD_REQUEST',
    the function returns errors.

    ...

    Parameters
    ----------
    username : str
        username value from RegisterForm
    email : str
        email value from RegisterForm (not required)
    password : str
        password value from RegisterForm
    re_password : str
        re_password value from RegisterForm
        (required if Settings.USER_CREATE_PASSWORD_RETYPE is True)

    """

    credential = {
        'username': username,
        'email': email,
        'password': password,
        're_password': re_password
    }
    response = requests.post(f'{AUTH_API_URL}users/', json=credential)
    if response.status_code == 201:
        return {'username': response.json()['username']}
    else:  # response.status_code == 400
        return {'errors': response.json()}


def pwd_reset_by_email(email):
    """
    Used to send email to user with password reset link.
    The function doesn't return information about  whether the attempt
    to send a email was successful, because it doesn't use in View.

    ...

    Parameters
    ----------
    email : str
        email value from PasswordResetForm

    """
    requests.post(f'{AUTH_API_URL}users/reset_password/', json={'email': email})


def pwd_reset_confirm(uidb64, token, password, re_password):
    """
    Used to finish reset password process.
    If response contains the status 'HTTP_204_NO_CONTENT', the function returns
    message about successful password change.
    If response contains the status 'HTTP_400_BAD_REQUEST', the function
    returns errors.

    ...

    Parameters
    ----------
    uidb64 : str
        uidb64 value from link in sended email
    token : str
        token value from link in sended email
    password : str
        new password value from PasswordResetConfirmForm
    re_password : str
        new re_password value from PasswordResetConfirmForm

    """
    credential = {
        'uid': uidb64,
        'token': token,
        'new_password': password,
        're_new_password': re_password
    }
    response = requests.post(f'{AUTH_API_URL}users/reset_password_confirm/', json=credential)
    if response.status_code == 204:
        return {'success': 'The password has been changed!'}
    else:  # response.status_code == 400
        for key in response.json():
            errors = response.json()[key]
        return {'errors': errors}
