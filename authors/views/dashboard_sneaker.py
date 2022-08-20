from authors.forms.sneaker_form import AuthorsSneakerForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from sneakers.models import Sneaker


@method_decorator(
    login_required(
        login_urls='authors:login',
        redirect_field_name='next'
    ),
    name='dispatch'
)
class DashboardSneaker(View):

    def get_sneaker(self, id=None):
        sneaker = None

        if id is not None:
            sneaker = Sneaker.objects.filter(
                is_published=False,
                author=self.request.user,
                pk=id,
            ).first()

            if not sneaker:
                raise Http404()

        return sneaker

    def render_sneaker(self, form):
        return render(
            self.request,
            'authors/pages/dashboard_sneaker.html',
            context={
                'form': form,
            }
        )

    def get(self, request, id=None):
        sneaker = self.get_sneaker(id)
        form = AuthorsSneakerForm(instance=sneaker)
        return self.render_sneaker(form)

    def post(self, request, id=None):
        sneaker = self.get_sneaker(id)

        form = AuthorsSneakerForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=sneaker
        )

        if form.is_valid():
            sneaker = form.save(commit=False)

            sneaker.author = request.user
            sneaker.sneaker_description_is_html = False
            sneaker.is_published = False

            sneaker.save()

            messages.success(request, 'Your sneaker was successfully saved!')
            return redirect(
                reverse('authors:dashboard_sneaker_edit', args=(sneaker.id,))
            )

        return self.render_sneaker(form)


@method_decorator(
    login_required(
        login_urls='authors:login',
        redirect_field_name='next'
    ),
    name='dispatch'
)
class DashboardSneakerDelete(DashboardSneaker):

    def post(self, *args, **kwargs):
        sneaker = self.get_sneaker(self.request.POST.get('id'))
        sneaker.delete()
        messages.success(self.request, 'Deleted successfully.')
        return redirect(reverse('authors:dashboard'))
