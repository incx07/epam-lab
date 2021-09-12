"""Custom JWT Authentication middleware."""

from django.urls import reverse
from django.contrib.sites.models import Site
from .service.auth_api_service import client


class JWTCheckMiddleware:
    '''
    The middleware is designed to check the user's permissions.
    If the cookie provided by the browser contains a refresh token,
    it is used to obtain a new access token.
    This logic should only be executed for the client side of the application
    (the path does not contain '/api/').
    Additionally, the full url will be saved (required in services).

    '''
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
    # Code to be executed for each request before
    # the view (and later middleware) are called.
        site = Site.objects.get(id=1)
        site.domain = request.build_absolute_uri(reverse('index'))
        site.save()
        if not '/api/' in request.path:
            if "refresh_token" in request.COOKIES:
                refresh_token = request.COOKIES["refresh_token"]
                client.refresh(refresh_token)
            else:
                client.is_authenticated = False
                client.username = None
                client.session.headers.clear()
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response
