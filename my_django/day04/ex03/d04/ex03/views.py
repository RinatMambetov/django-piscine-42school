from django.shortcuts import render

# Create your views here.

def index2(request):
    step = 255 / 50
    context = {
        "range": [
            "{:02X}".format(int(i * step)) for i in range(50)
        ]
    }
    return render(request, 'ex03/index.html', context)
