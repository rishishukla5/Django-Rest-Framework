from django.utils.deprecation import MiddlewareMixin
import uuid


class UUIDMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        # pass
        my_request = request.GET.copy()
        my_request['UUID'] = uuid.uuid4()
        request.GET = my_request
        return self.get_response(request)
