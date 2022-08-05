from django.views.generic import FormView
from ..forms import Login
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect, render


class MyFormView(FormView):
    template_name = 'ex00/login.html'
    form_class = Login
    success_url = '/'

    def get(self, request):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'You already logining!')
            return redirect('/')
        return super().get(request)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(self.request, 'Incorrect user or password')
            return render(self.request, self.template_name, {'form': form})
        login(self.request, user)
        return super().form_valid(form)



