from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Sneaker
from ..serializers import SneakerSerializer


@api_view()
def sneaker_api_list(request):
    sneakers = Sneaker.objects.get_published()[:10]
    serializer = SneakerSerializer(instance=sneakers, many=True)
    return Response(serializer.data)


@api_view()
def sneaker_api_detail(request, pk):
    sneaker = get_object_or_404(
        Sneaker.objects.get_published(),
        pk=pk
    )
    serializer = SneakerSerializer(instance=sneaker, many=False)
    return Response(serializer.data)
