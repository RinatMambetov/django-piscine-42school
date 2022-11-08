from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from ..models import UserFavouriteArticle
from django.contrib.auth.models import User


from django.contrib import messages


class FavoriteView(ListView):
    model = UserFavouriteArticle
    template_name = 'ex00/favorites.html'
    context_object_name = 'favorites'

    def get(self, request):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'You are not logining!')
            return redirect('/')
        return super().get(request)

    def get_queryset(self):
        print()
        return UserFavouriteArticle.objects.filter(user=self.request.user.id)
