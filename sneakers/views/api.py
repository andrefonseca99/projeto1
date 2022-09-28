from authors.models import Profile
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Sneaker
from ..serializers import ProfileSerializer, SneakerSerializer


class SneakerAPIv2Pagination(PageNumberPagination):
    page_size = 9


class SneakerAPIv2List(ListCreateAPIView):
    queryset = Sneaker.objects.get_published()
    serializer_class = SneakerSerializer
    pagination_class = SneakerAPIv2Pagination
    # def get(self, request):
    #     sneakers = Sneaker.objects.get_published()[:10]
    #     serializer = SneakerSerializer(
    #         instance=sneakers,
    #         many=True,
    #         context={'request': request},
    #     )
    #     return Response(serializer.data)

    # def post(self, request):
    #     serializer = SneakerSerializer(
    #         data=request.data,
    #         context={'request': request},
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(
    #         serializer.data,
    #         status=status.HTTP_201_CREATED
    #     )


class SneakerAPIv2Detail(APIView):
    def get_sneaker(self, pk):
        sneaker = get_object_or_404(  # noqa: F841
            Sneaker.objects.get_published(),
            pk=pk
        )
        return sneaker

    def get(self, request, pk):
        sneaker = self.get_sneaker(pk)
        serializer = SneakerSerializer(
            instance=sneaker,
            many=False,
            context={'request': request},
        )
        return Response(serializer.data)

    def patch(self, request, pk):
        sneaker = self.get_sneaker(pk)
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

    def delete(self, request, pk):
        sneaker = self.get_sneaker(pk)
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
