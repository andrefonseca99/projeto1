from django.http import Http404
from django.shortcuts import render
from utils.sneakers.factory import make_sneaker

from sneakers.models import Sneaker


def home(request):
    sneakers = Sneaker.objects.filter(is_published=True).order_by('-id')
    return render(request, 'sneakers/pages/home.html', context={
        'sneakers': sneakers,
    })



def category(request, category_id):
    sneakers = Sneaker.objects.filter(category__id=category_id, is_published=True).order_by('-id')

    if not sneakers:
        raise Http404('Not found')

    return render(request, 'sneakers/pages/category.html', context={
        'sneakers': sneakers,
        'title': f'{sneakers.first().category.name} - Category |'
    })

def sneaker(request, id):
    return render(request, 'sneakers/pages/sneaker-view.html', context={
        'sneaker': make_sneaker(),
        'is_detail_page': True,
    })
