from django.http import HttpResponse
from django.shortcuts import render
from utils.sneakers.factory import make_sneaker


def home(request):
    return render(request, 'sneakers/pages/home.html', context={
        'sneakers': [make_sneaker() for _ in range(11)],
    })


def sneaker(request, id):
    return render(request, 'sneakers/pages/sneaker-view.html', context={
        'sneaker': make_sneaker(),
        'is_detail_page': True,
    })
