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
from apps.linkedout import views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),

    # Sección de perfil y autenticación
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/manage/', views.manage_profile, name='manage_profile'),

    # Sección laboral
    path('search-jobs/', views.search_jobs, name='search_jobs'),
    path('apply-job/<int:job_id>/', views.apply_job, name='apply_job'),
    path('search-staff/', views.search_staff, name='search_staff'),
    path('create-post/', views.create_post, name='create_post'),
    path('post-job/', views.post_job, name='post_job'),
    path('professional-profile/<int:pk>/', views.professional_detail, name='professional_detail'),
    path('manage-staff/', views.manage_staff, name='manage_staff'),

    # Sección social
    path('feed/', views.feed, name='feed'),
    path('feed/follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('feed/comment/<int:post_id>/', views.comment_post, name='comment_post'),

    # Sección Mensajeria --- Por si acaso, aqui estaba el conflicto ---
    path('messages/', views.messages, name='messages'),
    path('messages/chat/<int:user_id>/', views.chat, name='chat'),
    path('notifications/', views.notifications_view, name='notifications'),

    # Sección de administración
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/users/manage/', views.manage_users, name='manage_users'),
    path('admin-panel/content/manage/', views.manage_content, name='manage_content'),
]
