from django.shortcuts import render
# from django.views.generic import FormView
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.views.generic.edit import CreateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


class Login(View):
    template_name = "account/login.html"
    form_class = AuthenticationForm
    # success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return render(
                request,
                self.template_name,
                {
                    "form": self.form_class(),
                    "username": request.user.username,
                }
            )
        else:
            return render(
                request,
                self.template_name,
                {
                    "form": self.form_class(),
                    "error": "request.user.username",
                }
            )

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is None:
            return JsonResponse(data={"error": 'Неудачная авторизация'},
                                status=200)
        login(request, user)

        return JsonResponse(data={"username": username}, status=200)


class Account(View):

    def get(self, request):
        if request.user.is_authenticated:
            # return JsonResponse(data={"username": request.user.username}, status=200)
            return render(request, 'account/login.html', context={"form": AuthenticationForm(), "username": request.user.username})
        return render(request, 'account/login.html', context={"form": AuthenticationForm()})

    def post(self, request):
        if request.user.is_authenticated:
            print(request.user.username)
            return JsonResponse(data={"username": request.user.username}, status=200)
        return JsonResponse(data={'status': 'error'}, status=200)


class CheckLogin(View):

    def get(self, request):
        if request.user.is_authenticated:
            print(request.user.username)
            return JsonResponse(data={"username": request.user.username}, status=200)
        return JsonResponse(data={'error': 'not auth'}, status=200)


class Logout(View):

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            request.session['mykey'] = 'myvalue'
            return JsonResponse(data={}, status=200)
        return JsonResponse(data={}, status=200)

