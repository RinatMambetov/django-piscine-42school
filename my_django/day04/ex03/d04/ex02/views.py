import logging
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.conf import settings
from . import forms
from datetime import datetime


def index(request: HttpRequest):
	logger = logging.getLogger('history')
	logging.basicConfig(format='%(asctime)s %(message)s')

	if request.method == 'POST':
		form = forms.History(request.POST)
		if form.is_valid():
			logger.warning(form.cleaned_data['history'])
			now = datetime.now()
			f = open(settings.HISTORY_LOG_FILE, 'a')
			f.write(form.cleaned_data['history'] + ' (' + now.strftime("%d/%m/%Y, %H:%M:%S") + ')\n')
			f.close
		return redirect('/ex02')
	try:
		f = open(settings.HISTORY_LOG_FILE, 'r')
		histories = [line for line in f.readlines()]
		f.close
	except:
		histories = []

	return render(request, 'ex02/index.html', {'form': forms.History(), 'histories': histories})
