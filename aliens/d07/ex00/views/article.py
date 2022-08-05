from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login
from django.views.generic import FormView
from django.contrib import messages
from django.shortcuts import render, redirect
from ..models import Article
from ..forms import Login

class MyListView(ListView, FormView):
    model = Article
    template_name = 'ex00/article.html'
    context_object_name = 'articles'
    form_class = Login
    success_url = '/'

    def get_queryset(self):
        return Article.objects.all()

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            return context
        except Exception:
            return redirect('/')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(self.request, 'Incorrect user or password')
            return redirect('/')
            return render(self.request, self.template_name, {'form': form})
        login(self.request, user)
        return super().form_valid(form)

