from django.shortcuts import render
# from django.http import HttpResponse
import random

# Create your views here.

def home(request):
	# return HttpResponse('Hello')

	return render(request, 'generator/home.html')

def password(request):
	# return HttpResponse('<h1>eggs</h1>')

	length = int(request.GET.get('length', 8)) #8 is default value

	characters = list('abcdefghijklmnopqrstuvwxyz')

	if request.GET.get('uppercase'):
		characters.extend(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

	if request.GET.get('special'):
		characters.extend(list('!@#$%^&*()_+-='))

	if request.GET.get('numbers'):
		characters.extend(list('0123456789'))

	thepassword = ''

	for x in range(length):
		thepassword += random.choice(characters)

	return render(request, 'generator/password.html', {'password': thepassword})

def description(request):
	return render(request, 'generator/description.html')
