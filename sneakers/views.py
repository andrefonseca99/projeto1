import os

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from utils.pagination import make_pagination

from sneakers.models import Sneaker

PER_PAGE = int(os.environ.get('PER_PAGE', 12))


def home(request):
    sneakers = Sneaker.objects.filter(
        is_published=True,
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, sneakers, PER_PAGE)

    return render(request, 'sneakers/pages/home.html', context={
        'sneakers': page_obj,
        'pagination_range': pagination_range,
    })


def category(request, category_id):
    sneakers = get_list_or_404(Sneaker.objects.filter(
        category__id=category_id,
        is_published=True,
    ).order_by('-id'))

    page_obj, pagination_range = make_pagination(request, sneakers, PER_PAGE)

    return render(request, 'sneakers/pages/category.html', context={
        'sneakers': page_obj,
        'pagination_range': pagination_range,
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
    search_term = request.GET.get('q', '').strip()  # Can return None
    if not search_term:
        raise Http404()

    sneakers = Sneaker.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ),
        is_published=True
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, sneakers, PER_PAGE)

    return render(request, 'sneakers/pages/search.html', {
        'page_title': f'Search for "{search_term} "|',
        'search_term': search_term,
        'sneakers': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}',
    })
