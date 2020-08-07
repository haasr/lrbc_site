"""Defines url patterns for the api app."""

from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'api'

# Update which pages are allowed when app starts.
views.update_pages_allowed()

urlpatterns = [
    path('views/charts/', views.views_charts_today, name='views_charts_today'),
    path('views/charts/<str:enddate>', views.views_charts_enddate, name='views_charts_enddate'),
    path('views/charts/export_views/', views.export_views, name='export_views'),
    path('views/data/delete/<str:time_period>/<str:enddate>', views.delete_views, name='delete_views'),
    path('visitors/charts/', views.visitors_charts_today, name='visitors_charts_today'),
    path('visitors/charts/<str:enddate>', views.visitors_charts_enddate, name='visitors_charts_enddate'),
    path('visitors/charts/export_visitors/', views.export_visitors, name='export_visitors'),
    path('visitors/data/delete/<str:time_period>/<str:enddate>', views.delete_visitors, name='delete_visitors'),
    path('views/data/daily/<str:enddate>/', login_required(views.DailyPageViews.as_view())),
    path('views/data/weekly/<str:enddate>/', login_required(views.WeeklyPageViews.as_view())),
    path('views/data/monthly/<str:enddate>/', login_required(views.MonthlyPageViews.as_view())),
    path('visitors/data/daily/<str:enddate>/', login_required(views.DailyVisitors.as_view())),
    path('visitors/data/weekly/<str:enddate>/', login_required(views.WeeklyVisitors.as_view())),
    path('visitors/data/monthly/<str:enddate>/', login_required(views.MonthlyVisitors.as_view())),
]