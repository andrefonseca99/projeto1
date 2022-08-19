from authors.forms.sneaker_form import AuthorsSneakerForm
from django.contrib import messages
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from sneakers.models import Sneaker


class DashboardSneaker(View):
    def get(self, request, id):
        sneaker = Sneaker.objects.filter(
            is_published=False,
            author=request.user,
            pk=id,
        ).first()

        if not sneaker:
            raise Http404()

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
                reverse('authors:dashboard_sneaker_edit', args=(id,))
            )

        return render(
            request,
            'authors/pages/dashboard_sneaker.html',
            context={
                'form': form,
            }
        )
