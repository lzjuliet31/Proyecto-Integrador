"""
URL configuration for backend project.

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
# backend/urls.py
from django.contrib import admin
from django.urls import path
from api.views import (
    RolListView,
    UsuarioListView,
    PersonalExternoListView,
    RegistroUsuarioView,
    LoginDNIView,
    RegistrarPatrullaView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # AUTH
    path("login/", LoginDNIView.as_view()),
    path("usuarios/crear/", RegistroUsuarioView.as_view()),

    # LISTADOS
    path("roles/", RolListView.as_view()),
    path("usuarios/", UsuarioListView.as_view()),
    path("personal/", PersonalExternoListView.as_view()),

    # SISTEMA DE PATRULLA
    path("patrulla/registrar/", RegistrarPatrullaView.as_view()),
]

