from django.shortcuts import render

# Create your views here.

def	ex00(request):
	return render(request, 'ex00/index.html')
