from .service.auth import client

class JWTCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
    # Code to be executed for each request before
    # the view (and later middleware) are called.
        if not 'api' in request.path:
            if "refresh_token" in request.COOKIES:
                refresh_token = request.COOKIES["refresh_token"]
                print(request.path)
                client.refresh(refresh_token)
            else:
                print(request.path)
                client.is_authenticated = False
                print(client.is_authenticated)
                client.username = None
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response
