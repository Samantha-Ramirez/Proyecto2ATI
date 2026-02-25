from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


def admin_panel(request):
    return render(request, 'admin_panel.html')


def manage_users(request):
    return render(request, 'manage_users.html')


def manage_content(request):
    return render(request, 'manage_content.html')
