from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.OptionsView.as_view(), name='options'),
    path('load_game', views.LoadView.as_view(), name='load_game'),
    path('save_game', views.SaveView.as_view(), name='save_game'),
]
