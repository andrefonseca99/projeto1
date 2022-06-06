from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'sneakers/pages/home.html', context={
        'name': 'André',
    })


def sneaker(request, id):
    return render(request, 'sneakers/pages/sneaker-view.html', context={
        'name': 'André',
    })
