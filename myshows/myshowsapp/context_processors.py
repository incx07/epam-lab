from .service.auth_api_service import client


def client_auth(request):
    """A context processor that provides 'is_authenticated' and 'username'."""
    return {
        'is_authenticated': client.is_authenticated,
        'username': client.get_username()
    }
