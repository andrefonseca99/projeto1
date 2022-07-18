from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from utils.pagination import make_pagination_range

from sneakers.models import Sneaker

# from utils.sneakers.factory import make_sneaker


def home(request):
    sneakers = Sneaker.objects.filter(
        is_published=True,
    ).order_by('-id')

    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    paginator = Paginator(sneakers, 12)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        4,
        current_page
    )

    return render(request, 'sneakers/pages/home.html', context={
        'sneakers': page_obj,
        'pagination_range': pagination_range,
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

    return render(request, 'sneakers/pages/search.html', {
        'page_title': f'Search for "{search_term} "|',
        'search_term': search_term,
        'sneakers': sneakers,
    })
