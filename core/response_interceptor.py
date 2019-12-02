from django.conf import settings
from django.middleware.common import CommonMiddleware


class AuthMiddleware(CommonMiddleware):
    def process_response(self, request, response):
        print("decorating response object with privileges for UI to use")
        if not request.user.is_authenticated:
            return response
        response.META["privileges"] = request.user.Meta.groups
        return response
