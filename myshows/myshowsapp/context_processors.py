"""
A set of request processors that return dictionaries to be merged into a
template context. Each function takes the request object as its only parameter
and returns a dictionary to add to the context.
These are referenced from the setting TEMPLATE_CONTEXT_PROCESSORS and used by
RequestContext.
"""

from .service.auth_api_service import client


def client_auth(request):
    """
    It required by apps that use JWT Authentication system.
    Adds context variables with information about current user to the context.
    """
    return {
        'is_authenticated': client.is_authenticated,
        'username': client.get_username()
    }
