from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


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
