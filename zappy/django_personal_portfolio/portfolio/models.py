from django.db import models


class Project(models.Model):
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=250)
	image = models.ImageField(upload_to='portfolio/images/')
	url = models.URLField(blank=True)	#blank means its maybe empty


	def __str__(self):
		# return self.title + ' ' + self.description
		return self.title
