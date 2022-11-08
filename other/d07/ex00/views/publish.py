from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from ..models import Article
from ..forms import PublishForm
from django.contrib import messages


class PublishView(ListView):
    template_name = 'ex00/publish.html'
    context_object_name = 'favorites'


    def get(self, request):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'You are not logining!')
            return redirect('/')
        context = {'form': PublishForm()}
        return render(request, self.template_name, context)

    def post(self, request):
        data = PublishForm(request.POST)
        if data.is_valid():
            try:
                Article.objects.get(title=data.cleaned_data['title'])
            except Exception:
                Article.objects.create(title=data.cleaned_data['title'],
                       author_id=request.user.id,
                       synopsis=data.cleaned_data['synopsis'],
                       content=data.cleaned_data['content'])
                return redirect('/')
        return render(request, self.template_name, {'form': data})

