import os

from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import Http404, JsonResponse
from django.views.generic import DetailView, ListView
from utils.pagination import make_pagination

from sneakers.models import Sneaker

PER_PAGE = int(os.environ.get('PER_PAGE', 12))


class SneakerListViewBase(ListView):
    model = Sneaker
    context_object_name = 'sneakers'
    paginate_by = None
    ordering = ['-id']
    template_name = 'sneakers/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
        qs = qs.select_related('author', 'category')
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('sneakers'),
            PER_PAGE
        )
        ctx.update(
            {'sneakers': page_obj, 'pagination_range': pagination_range}
        )
        return ctx


class SneakerListViewHome(SneakerListViewBase):
    template_name = 'sneakers/pages/home.html'


class SneakerListViewHomeAPI(SneakerListViewBase):
    template_name = 'sneakers/pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        sneakers = self.get_context_data()['sneakers']
        sneakers_list = sneakers.object_list.values()

        return JsonResponse(
            list(sneakers_list),
            safe=False
        )


class SneakerListViewCategory(SneakerListViewBase):
    template_name = 'sneakers/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_id'),
            is_published=True,
        ).order_by('-id')
        if not qs:
            raise Http404()
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'title': f'{ctx.get("sneakers")[0].category.name} - Category |'
        })
        return ctx


class SneakerListViewSearch(SneakerListViewBase):
    template_name = 'sneakers/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404()

        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
            ),
            is_published=True,
            ).order_by('-id')
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')
        ctx.update({
            'page_title': f'Search for "{search_term} "|',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
        })
        return ctx


class SneakerDetailView(DetailView):
    model = Sneaker
    context_object_name = 'sneaker'
    template_name = 'sneakers/pages/sneaker-view.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'is_detail_page': True,
        })
        return ctx

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs


class SneakerDetailAPI(SneakerDetailView):
    def render_to_response(self, context, **response_kwargs):
        sneaker = self.get_context_data()['sneaker']
        sneaker_dict = model_to_dict(sneaker)

        sneaker_dict['created_at'] = str(sneaker.created_at)

        if sneaker_dict.get('cover'):
            sneaker_dict['cover'] = self.request.build_absolute_uri() + \
                 sneaker_dict['cover'].url[1:]
        else:
            sneaker_dict['cover'] = ''

        del sneaker_dict['is_published']

        return JsonResponse(
            sneaker_dict,
            safe=False,
        )
