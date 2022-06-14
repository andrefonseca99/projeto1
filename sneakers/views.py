from django.http import HttpResponse
from django.shortcuts import render
from utils.sneakers.factory import make_sneaker

from sneakers.models import Sneaker


def home(request):
    sneakers = Sneaker.objects.all().order_by('-id')
    return render(request, 'sneakers/pages/home.html', context={
        'sneakers': sneakers,
    })

def category(request, category_id):
    sneakers = Sneaker.objects.filter(category__id=category_id).order_by('-id')
    return render(request, 'sneakers/pages/home.html', context={
        'sneakers': sneakers,
    })

def sneaker(request, id):
    return render(request, 'sneakers/pages/sneaker-view.html', context={
        'sneaker': make_sneaker(),
        'is_detail_page': True,
    })
