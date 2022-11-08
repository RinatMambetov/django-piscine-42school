from . import views
from django.urls import path, include

urlpatterns = [
	path('', views.IndexView.as_view(), name='mainpage'),
]
