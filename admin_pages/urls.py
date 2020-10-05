"""Defines url patterns for the admin_pages app."""

from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'admin_pages'

urlpatterns = [
    path('', views.admin_index, name='admin_index'),
    path('manage_site_look/', views.manage_site_look, name='manage_site_look'),
    path('manage_home/', views.manage_home, name='manage_home'),
    path('manage_about/', views.manage_about, name='manage_about'),
    path('manage_leadership/', views.manage_leadership, name='manage_leadership'),
    path('manage_leadership_header/', views.manage_leadership_header, name='manage_leadership_header'),
    path('manage_resources/', views.manage_resources, name='manage_resources'),
    path('manage_sermons_header/', views.manage_sermons_header, name='manage_sermons_header'),
    path('manage_worship_music_header/', views.manage_worship_music_header, name='manage_worship_music_header'),
    path('manage_worship_videos_header/', views.manage_worship_videos_header, name='manage_worship_videos_header'),
    path('manage_services/', views.manage_services, name='manage_services'),
    path('manage_contact/', views.manage_contact, name='manage_contact'),
    path('manage_seo/', views.manage_seo, name='manage_seo'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('manage_email_account/', views.manage_email_account, name='manage_email_account'),
    path('manage_ip_nolog_list/', views.manage_ip_nolog_list, name='manage_ip_nolog_list'),
    path('manage_email_denylist/', views.manage_email_denylist, name='manage_email_denylist'),

    path('new_leader/', views.new_leader, name='new_leader'),
    path('edit_leader/<int:leader_id>', views.edit_leader, name='edit_leader'),
    path('delete_leader/<int:leader_id>', views.delete_leader, name='delete_leader'),

    path('new_speaker/', views.new_speaker, name='new_speaker'),
    path('edit_speaker/<int:speaker_id>/', views.edit_speaker, name='edit_speaker'),
    path('confirm_delete_speaker/<int:speaker_id>/', views.confirm_delete_speaker, name='confirm_delete_speaker'),
    path('delete_speaker/<int:speaker_id>/', views.delete_speaker, name='delete_speaker'),

    path('new_artist/', views.new_artist, name='new_artist'),
    path('edit_artist/<int:artist_id>/', views.edit_artist, name='edit_artist'),
    path('confirm_delete_artist/<int:artist_id>/', views.confirm_delete_artist, name='confirm_delete_artist'),
    path('delete_artist/<int:artist_id>/', views.delete_artist, name='delete_artist'),

    path('new_sermon/<int:speaker_id>/', views.new_sermon, name='new_sermon'),
    path('edit_sermon/<int:sermon_id>/', views.edit_sermon, name='edit_sermon'),
    path('delete_sermon/<int:sermon_id>/', views.delete_sermon, name='delete_sermon'),

    path('new_song/<int:artist_id>/', views.new_song, name='new_song'),
    path('edit_song/<int:song_id>/', views.edit_song, name='edit_song'),
    path('delete_song/<int:song_id>/', views.delete_song, name='delete_song'),

    path('new_worship_video/<int:speaker_id>/', views.new_worship_video, name='new_worship_video'),
    path('edit_worship_video/<int:video_id>/', views.edit_worship_video, name='edit_worship_video'),
    path('delete_worship_video/<int:video_id>/', views.delete_worship_video, name='delete_worship_video'),

    path('new_nolog_ip/', views.new_nolog_ip, name='new_nolog_ip'),
    path('edit_nolog_ip/<int:nologip_id>/', views.edit_nolog_ip, name='edit_nolog_ip'),
    path('delete_nolog_ip/<int:nologip_id>/', views.delete_nolog_ip, name='delete_nolog_ip'),

    path('new_denylistemail/', views.new_denylistemail, name='new_denylistemail'),
    path('edit_denylistemail/<int:denylistemail_id>/', views.edit_denylistemail, name='edit_denylistemail'),
    path('delete_denylistemail/<int:denylistemail_id>/', views.delete_denylistemail, name='delete_denylistemail'),
]
