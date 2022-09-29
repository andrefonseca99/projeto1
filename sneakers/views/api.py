from authors.models import Profile
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..models import Sneaker
from ..serializers import ProfileSerializer, SneakerSerializer


class SneakerAPIv2Pagination(PageNumberPagination):
    page_size = 9


class SneakerAPIv2ViewSet(ModelViewSet):
    queryset = Sneaker.objects.get_published()
    serializer_class = SneakerSerializer
    pagination_class = SneakerAPIv2Pagination

    def get_queryset(self):
        qs = super().get_queryset()
        category_id = self.request.query_params.get('category_id', '')

        if category_id != '' and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)

        return qs


@api_view()
def profile_api_detail(request, pk):
    profile = get_object_or_404(
        Profile.objects.all(),
        pk=pk
    )
    serializer = ProfileSerializer(
        instance=profile,
        many=False,
        context={'request': request},
    )
    return Response(serializer.data)
