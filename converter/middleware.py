import logging

logger = logging.getLogger('django.request')

class LogRequestHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Логируем заголовки запроса
        logger.info(f"Request Headers: {dict(request.headers)}")
        response = self.get_response(request)
        return response
