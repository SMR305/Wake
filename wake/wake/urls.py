"""
URL configuration for wake project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path, re_path
from . import views
from .models import Server

servers = list(Server.objects.values("name"))

urlpatterns = [
    path('', views.index, name='home'),
    path("desktop/", views.toggle_button, name="desktop"),
    path("other/", views.toggle_button, name="other"),
    re_path(r"^add/[a-zA-Z0-9_-]{1,100}/$", views.add, name="add"),
    re_path(r"^power/[a-zA-Z0-9_-]{1,100}/$", views.power, name="power"),
    re_path(r"^reboot/[a-zA-Z0-9_-]{1,100}/$", views.reboot, name="reboot"),
    re_path(r"^delete/[a-zA-Z0-9_-]{1,100}/$", views.delete, name="delete"),
]
