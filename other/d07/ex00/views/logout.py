from django.contrib.auth.views import LogoutView


class MyLogout(LogoutView):
    next_page = '/'

