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
    path('browse/', views.browse_food, name='browse_food'),
    path('claim/<uuid:donation_id>/', views.claim_food, name='claim_food'),
    path('history/', views.ngo_history, name='ngo_history'),
    path('verify/', views.verify_pickup, name='verify_pickup'),
    path('upload-media/', views.upload_ngo_media, name='upload_ngo_media'),
]