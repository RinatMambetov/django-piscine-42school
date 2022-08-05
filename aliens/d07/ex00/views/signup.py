from django.views.generic import CreateView
from ..forms import Signup
from django.shortcuts import render, redirect
from django.contrib import messages


class MySignup(CreateView):
    template_name = 'ex00/signup.html'

    def get(self, request):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'You already logining!')
            return redirect('/')
        context = {'form_reg': Signup()}
        return render(request, self.template_name, context)

    def post(self, request):
        print(self.kwargs)
        data = Signup(request.POST)
        if data.is_valid():
            data.save()
            return redirect('login')
        else:
            return render(request, self.template_name, {'form_reg': data})
