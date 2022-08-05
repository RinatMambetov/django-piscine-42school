from django.urls import path
from . import views

urlpatterns = [
	path('populate/', views.Populate.as_view(), name='ex07-populate'),
	path('display/', views.Display.as_view(), name='ex07-display'),
	path('update/', views.Update.as_view(), name='ex07-remove'),
]
