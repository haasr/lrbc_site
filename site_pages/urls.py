"""Defines url patterns for the site_pages app."""

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('sermons/', views.sermons, name='sermons'),
    path('worship_music/', views.worship_music, name='worship_music'),
    path('worship_videos/', views.worship_videos, name='worship_videos'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('submit_contact_email/', views.submit_contact_email, name='submit_contact_email'),
    path('submit_prayer_request/', views.submit_prayer_request, name='submit_prayer_request'),
    path('submit_contact_form/', views.sumbit_contact_form, name='submit_contact_form'),
]
