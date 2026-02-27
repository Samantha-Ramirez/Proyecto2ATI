from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        public_urls = [
            reverse('login'),
            reverse('register'),
            '/admin/',
            '/i18n/',
        ]

        if not request.user.is_authenticated:
            if not any(request.path.startswith(url) for url in public_urls):
                return redirect('login')

        return self.get_response(request)
