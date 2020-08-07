"""Defines url patterns for the users app."""

from django.urls import path
from django.contrib.auth import login, views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html'), name='login'),

	path('logout/', views.logout_view, name='logout'),
	path('register/', views.register, name='register'),
	path('confirm_delete_user/<int:user_id>/', views.confirm_delete_user, name='confirm_delete_user'),
	path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
]
