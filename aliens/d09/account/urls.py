from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    path('', views.Account.as_view(), name='contact_form'),
    path('check-login/', views.CheckLogin.as_view(), name='check_login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('login/', views.Login.as_view(), name='login'),
]
