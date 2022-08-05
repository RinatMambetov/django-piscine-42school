from django.contrib import auth
from django.contrib.auth.decorators import login_required
from random import choice
from ex.models import Tip
from ex.forms import *
from django.shortcuts import render, redirect
from django.conf import settings


def main(request):
    form = TipForm()

    response = render(request, 'ex/base.html')
    if not request.COOKIES.get('username'):
        random_user = choice(settings.USER_POOL)
        request.COOKIES['username'] = random_user
        response = render(request, 'ex/base.html')
        response.set_cookie('username', random_user, max_age=42)
    if request.user.is_authenticated:
        if request.method == 'POST':
            tmpform = TipForm(request.POST)
            if tmpform.is_valid():
                tip = Tip(content=request.POST.get('content'), author=request.user)
                tip.save()
        tips = Tip.objects.all()
        return render(request, 'ex/base.html', {'tips': tips, 'form': form})
    return response


def login(request):
    form = LoginForm()

    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(
                username=request.POST['username'],
                password=request.POST['password']
            )
            auth.login(request, user)
            return redirect('/')

    return render(request, 'ex/login.html', {'form': form})


def register(request):
    form = RegisterForm()

    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = auth.get_user_model().objects.create_user(
                username=request.POST['username'],
                password=request.POST['password']
            )
            auth.login(request, user)
            return redirect('/')
    return render(request, 'ex/register.html', {'form': form})


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')
