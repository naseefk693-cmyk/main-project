"""
URL configuration for FOOD_DONATION project.

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
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('delete_donation/<uuid:donation_id>/', views.delete_donation, name='delete_donation'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('edit_donation/<uuid:donation_id>/', views.edit_donation, name='edit_donation'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('view_donation/<uuid:donation_id>/', views.view_donation, name='view_donation'),
    path('view_user/<int:user_id>/', views.view_user, name='view_user'),
    path('search_donations/', views.search_donations, name='search_donations'),
    path('search_users/', views.search_users, name='search_users'),
    path('filter_donations/', views.filter_donations, name='filter_donations'),
    path('filter_users/', views.filter_users, name='filter_users'),
    path('sort_donations/', views.sort_donations, name='sort_donations'),
    path('sort_users/', views.sort_users, name='sort_users'),
    path('delete_media/<int:media_id>/', views.delete_media, name='delete_media'),
]
