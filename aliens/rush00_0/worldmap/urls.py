from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.WorldmapView.as_view(), name='worldmap'),
]
