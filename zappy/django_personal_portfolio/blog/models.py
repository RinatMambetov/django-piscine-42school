from django.db import models


class Blog(models.Model):
	title = models.CharField(max_length=200)
	date = models.DateField()
	description = models.TextField(max_length=2000)


	def __str__(self):
		return self.title
