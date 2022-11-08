from . import views
from django.urls import path, include
app_name = 'moviedex'
urlpatterns = [
    path('', views.MoviedexView.as_view(), name='index'),
    path('<slug:movie_id>/', views.MoviedexDetailView.as_view(), name='detail')
]
