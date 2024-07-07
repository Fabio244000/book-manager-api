from rest_framework.response import Response
from functools import wraps


class APIResponse(Response):
    """
    Custom API response class to standardize the response format.
    """
    def __init__(self, success=True, message="", data=None, status=None, headers=None, content_type=None):

        response_data = {
            "success": success,
            "message": message,
            "data": data,
        }
        super().__init__(
            data=response_data,
            status=status,
            headers=headers,
            content_type=content_type,
        )


def api_response(success_message, error_message):
    """
    Decorator to handle API responses in a standardized format.

    Args:
        success_message (str): Message to be included in the response on success.
        error_message (str): Message to be included in the response on error.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                if result is None:
                    return APIResponse(
                        success=False,
                        message=error_message,
                        data=[],
                        status=500,
                    )
                if isinstance(result, list) and not result:
                    return APIResponse(
                        success=True,
                        message=success_message,
                        data=[],
                        status=200,
                    )
                return APIResponse(
                    success=True,
                    message=success_message,
                    data=result,
                    status=200,
                )
            except Exception as e:
                return APIResponse(
                    success=False,
                    message=f"{error_message}: {str(e)}",
                    data=[],
                    status=500,
                )
        return wrapper
    return decorator
