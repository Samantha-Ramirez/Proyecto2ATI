from django.shortcuts import render


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def profile(request):
    return render(
        request,
        'profile.html',
        {
            'page_title': 'Perfil',
            'show_bottom_nav': True,
            'desktop_search': True,
        },
    )


def manage_profile(request):
    return render(request, 'manage_profile.html')
