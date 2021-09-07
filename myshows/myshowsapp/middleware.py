"""JWT Authentication middleware."""

from .service.auth_api_service import client

class JWTCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
    # Code to be executed for each request before
    # the view (and later middleware) are called.
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
