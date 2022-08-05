
from ..models import Article, UserFavouriteArticle
from django.shortcuts import redirect, render
from django.contrib import messages


def DetailView(request, catid=None):
    if not request.user.is_authenticated:
        messages.error(request, 'You are not logining!')
        return redirect('/')
    if catid is None or not request.user.is_authenticated:
        return redirect('/ex00/publications/')
    if request.method == 'POST':
        val = request.POST['add']
        lst = UserFavouriteArticle.objects.filter(user=request.user.id).filter(article=val)
        if not lst:
            UserFavouriteArticle.objects.create(user_id=request.user.id,article=Article.objects.get(id=val))
            return redirect('favorite')
        messages.error(request, 'That article already in your favorite list!')
        return redirect(request.path)
    else:
        try:
            art = Article.objects.get(id=catid)
            return render(request, 'ex00/details.html', {'article': art})
        except Exception:
            messages.error(request, f'Article with id {catid} does not exists!')
            return redirect('/ex00/publications/')
