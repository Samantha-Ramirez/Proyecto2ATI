from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


# Sección de perfil y autenticación
def login(request):
    return render(request, 'login.html.html')


def register(request):
    return render(request, 'register.html')


def profile(request):
    return render(request, 'profile.html')


def manage_profile(request):
    return render(request, 'manage_profile.html')


# Sección de zona laboral
def search_jobs(request):
    return render(request, 'search_jobs.html')


def apply_job(request, job_id):
    pass


def search_staff(request):
    return render(request, 'search_staff.html')


def post_job(request):
    return render(request, 'post_job.html')


# Sección de muro y mensajería
def feed_view(request):
    return render(request, 'feed.html')


def follow_user(request, user_id):
    pass


def comment_post(request, post_id):
    pass


def messages_view(request):
    return render(request, 'messages.html')


def chat_view(request, user_id):
    return render(request, 'chat.html')

# Sección de administración


def admin_panel(request):
    return render(request, 'admin_panel.html')


def manage_users(request):
    return render(request, 'manage_users.html')


def manage_content(request):
    return render(request, 'manage_content.html')
