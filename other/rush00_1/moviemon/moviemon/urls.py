from django.urls import path
from . import views


urlpatterns = [
    path('', views.title_screen, name='title_screen'),
    path('worldmap/new_game/', views.worldmap, name='worldmap'),
    path('worldmap/<str:direction>', views.worldmap, name='worldmap'),
    path('worldmap/', views.worldmap, name='worldmap'),
    path('battle/<str:moviemon_id>', views.battle, name='battle'),
    path('moviedex/<str:moviemon>', views.detail, name='detail'),
    path('battle/<str:moviemon_id>/throw', views.battle, name='battle'),
    path('moviedex/', views.moviedex, name='moviedex'),
    path('options/save_game/<str:save_file_name>', views.save, name='save_game'),
    path('options/save_game/', views.save, name='save_game'),
    path('options/load_game/<str:save_file_name>', views.load, name='load_game'),
    path('options/load_game/', views.load, name='load_game'),
    path('options/', views.option, name='options'),
    # path('', views.title_screen, name='index'),
]
