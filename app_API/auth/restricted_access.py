from flask import request, abort
from functools import wraps

from app_API.auth.auth import AuthError

ALLOWED_IPS = ['127.0.0.1']

# Wrapper function to restrict access to an endpoint
def restrict_access(endpoint):
    @wraps(endpoint)
    def wrapper(*args, **kwargs):
        # Check the IP address or application credentials here
        client_ip = request.remote_addr
        if client_ip not in ALLOWED_IPS:
            raise AuthError({
                'code': 'unauthorized',
                'description': 'Access restricted.'
            },403)
        return endpoint(*args, **kwargs)
    return wrapper