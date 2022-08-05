from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class Article(models.Model):
    title = models.CharField(max_length=64, null=False)
    author = models.ForeignKey(get_user_model(), null=False, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=False)
    synopsis = models.CharField(max_length=312, null=False)
    content = models.CharField(null=False, max_length=10000)

    def __str__(self):
        return self.title

    def get_dt(self):
        return self.created


class UserFavouriteArticle(models.Model):
    user = models.ForeignKey(get_user_model(), null=False, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.article.title


