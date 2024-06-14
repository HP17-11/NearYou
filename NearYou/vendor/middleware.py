# myapp/middleware.py

from django.utils.deprecation import MiddlewareMixin

class RememberLastVisitedMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path_info != '/logout/' and request.method == 'GET':
            request.session['last_visited_url'] = request.get_full_path()
        return response
