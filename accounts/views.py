from django.shortcuts import render


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def profile(request):
    return render(request, 'profile.html')


def manage_profile(request):
    return render(request, 'manage_profile.html')
