from django.urls import path
from .views.article import MyListView
from .views.login import MyFormView
from .views.logout import MyLogout
from .views.signup import MySignup
from .views.publications import PublicsView
from .views.detail import DetailView
from .views.favorite import FavoriteView
from .views.publish import PublishView

urlpatterns = [
    path('articles/', MyListView.as_view(), name='listview'),
    path('login/', MyFormView.as_view(), name='login'),
    path('logout/', MyLogout.as_view(), name='logout'),
    path('signup/', MySignup.as_view(), name='signup'),
    path('publications/', PublicsView.as_view(), name='publics'),
    path('favorites/', FavoriteView.as_view(), name='favorite'),
    path('detail/<int:catid>/', DetailView),
    path('publish/', PublishView.as_view(), name='publish'),

]



