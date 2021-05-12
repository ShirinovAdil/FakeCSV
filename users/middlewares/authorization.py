from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class LoginRequiredMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.user.is_authenticated and request.path != reverse_lazy(
            "login"
        ):
            return HttpResponseRedirect(reverse_lazy("login"))

        return response
