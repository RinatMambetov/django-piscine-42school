from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from ..models import Article


from django.contrib import messages


class PublicsView(ListView):
    model = Article
    template_name = 'ex00/publications.html'
    context_object_name = 'publics'

    def get(self, request):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'You are not logining!')
            return redirect('/')
        return super().get(request)

    def get_queryset(self):
        return Article.objects.filter(author_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
