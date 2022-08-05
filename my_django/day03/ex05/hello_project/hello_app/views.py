from django.shortcuts import render

# Create your views here.

def helloworld(request):
	return render(request, 'hello_app/helloworld.html')

def home(request):
	return render(request, 'hello_app/home.html')
