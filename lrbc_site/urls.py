"""lrbc_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('admin_pages/', include('admin_pages.urls')),
    path('api/', include('api.urls')),
    path('', include('site_pages.urls')),
    path('users/', include('users.urls')),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
            template_name='users/reset_password.html'), name='password_reset_confirm'),
    path('reset_password_done', auth_views.PasswordResetDoneView.as_view(
            template_name='users/reset_password_sent.html'), name='password_reset_done'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
            template_name='users/reset_password_complete.html'), name='password_reset_complete'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]