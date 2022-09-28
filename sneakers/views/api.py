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
            context={'request': request},
        )
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SneakerSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


@api_view(http_method_names=['get', 'patch', 'delete'])
def sneaker_api_detail(request, pk):
    sneaker = get_object_or_404(
        Sneaker.objects.get_published(),
        pk=pk
    )
    if request.method == 'GET':
        serializer = SneakerSerializer(
            instance=sneaker,
            many=False,
            context={'request': request},
        )
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = SneakerSerializer(
            instance=sneaker,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data
        )

    elif request.method == 'DELETE':
        sneaker.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
