from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from sneakers.models import Sneaker

# from utils.sneakers.factory import make_sneaker


def home(request):
    sneakers = Sneaker.objects.filter(
        is_published=True,
    ).order_by('-id')

    return render(request, 'sneakers/pages/home.html', context={
        'sneakers': sneakers,
    })


def category(request, category_id):
    sneakers = get_list_or_404(Sneaker.objects.filter(
        category__id=category_id,
        is_published=True,
    ).order_by('-id'))

    return render(request, 'sneakers/pages/category.html', context={
        'sneakers': sneakers,
        'title': f'{sneakers[0].category.name} - Category |'
    })


def sneaker(request, id):
    sneaker = get_object_or_404(Sneaker, pk=id, is_published=True,)

    return render(request, 'sneakers/pages/sneaker-view.html', context={
        'sneaker': sneaker,
        'is_detail_page': True,
    })


def search(request):
    # Checking if we have anything in the search form
    search_term = request.GET.get('q', '').strip()  # Returns None if we dont have 'q'
    if not search_term:
        raise Http404()

    return render(request, 'sneakers/pages/search.html', {
        'page_title': f'Search for "{search_term} "|',
        'search_term': search_term,
    })
