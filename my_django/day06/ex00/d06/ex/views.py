from random import choice
from django.shortcuts import render
from django.conf import settings

def main(request):
    response = render(request, 'ex/base.html')
    if not request.COOKIES.get('username'):
        random_user = choice(settings.USER_POOL)
        request.COOKIES['username'] = random_user
        response = render(request, 'ex/base.html')
        response.set_cookie('username', random_user, max_age=42)
    return response
