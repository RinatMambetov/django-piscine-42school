from . import views
from django.urls import path, include

urlpatterns = [
	path('<str:moviemon_id>', views.BattleView.as_view(), name='battle'),
]
