from authors.models import Profile
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Sneaker
from ..serializers import ProfileSerializer, SneakerSerializer


@api_view(http_method_names=['get', 'post'])
def sneaker_api_list(request):
    if request.method == 'GET':
        sneakers = Sneaker.objects.get_published()[:10]
        serializer = SneakerSerializer(
            instance=sneakers,
            many=True,
            context={'request': 'request'},
        )
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SneakerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.validated_data,
            status=status.HTTP_201_CREATED
        )


@api_view()
def sneaker_api_detail(request, pk):
    sneaker = get_object_or_404(
        Sneaker.objects.get_published(),
        pk=pk
    )
    serializer = SneakerSerializer(
        instance=sneaker,
        many=False,
        context={'request': 'request'},
    )
    return Response(serializer.data)


@api_view()
def profile_api_detail(request, pk):
    profile = get_object_or_404(
        Profile.objects.all(),
        pk=pk
    )
    serializer = ProfileSerializer(
        instance=profile,
        many=False,
        context={'request': 'request'},
    )
    return Response(serializer.data)
