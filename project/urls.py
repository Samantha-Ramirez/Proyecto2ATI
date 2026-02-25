"""
URL configuration for project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from apps.linkedout import controllers

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),

    # Sección de perfil y autenticación
    path('login/', controllers.login, name='login'),
    path('register/', controllers.register, name='register'),
    path('profile/', controllers.profile, name='profile'),
    path('profile/manage/', controllers.manage_profile, name='manage_profile'),

    # Sección de zona laboral
    path('search-jobs/', controllers.search_jobs, name='search_jobs'),
    path('apply-job/<int:job_id>/', controllers.apply_job, name='apply_job'),
    path('search-staff/', controllers.search_staff, name='search_staff'),
    path('post-job/', controllers.post_job, name='post_job'),

    # Sección de muro y mensajería
    path('feed/', controllers.feed, name='feed'),
    path('feed/follow/<int:user_id>/', controllers.follow_user, name='follow_user'),
    path('feed/comment/<int:post_id>/', controllers.comment_post, name='comment_post'),
    path('messages/', controllers.messages, name='messages'),
    path('messages/chat/<int:user_id>/', controllers.chat, name='chat'),

    # Sección de administración
    path('admin-panel/', controllers.admin_panel, name='admin_panel'),
    path('admin-panel/users/manage/', controllers.manage_users, name='manage_users'),
    path('admin-panel/content/manage/', controllers.manage_content, name='manage_content'),
]
