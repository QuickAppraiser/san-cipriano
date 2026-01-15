"""
Core utility functions for the San Cipriano project.
"""


def get_client_ip(request):
    """
    Extract client IP address from request.
    Handles X-Forwarded-For header for proxied requests.

    Args:
        request: Django HTTP request object

    Returns:
        str: Client IP address
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")
