from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import ChatRoom


@login_required(login_url='login')
def index(request):
    rooms = ChatRoom.objects.all().values_list('name', flat=True)
    context = {'rooms': rooms}
    return render(request, 'chat/index.html', context=context)


@login_required(login_url='login')
def room(request, room_name):
    rooms = ChatRoom.objects.all().values_list('name', flat=True)
    if room_name in rooms:
        return render(request, 'chat/room.html', {
            'room_name': room_name,
            'rooms': rooms,
        })
    else:
        return redirect('chat')
