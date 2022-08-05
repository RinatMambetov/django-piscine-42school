"""d04 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from ex00.views import ex00
from ex01.views import django
from ex01.views import display
from ex01.views import templates

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ex00/', ex00, name='ex00'),
    path('ex01/django/', django, name='django'),
    path('ex01/display/', display, name='display'),
    path('ex01/templates/', templates, name='templates'),
]
