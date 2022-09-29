from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from sneakers import views

# sneakers:sneaker
app_name = 'sneakers'

sneaker_api_v2_router = SimpleRouter()
sneaker_api_v2_router.register(
    'sneakers/api/v2',
    views.SneakerAPIv2ViewSet,
    basename='sneakers-api'
)

urlpatterns = [
    path(
        '',
        views.SneakerListViewHome.as_view(),
        name="home"
    ),
    path(
        'sneakers/search/',
        views.SneakerListViewSearch.as_view(),
        name="search"
    ),
    path(
        'sneakers/category/<int:category_id>/',
        views.SneakerListViewCategory.as_view(),
        name="category"
    ),
    path(
        'sneakers/<int:pk>/',
        views.SneakerDetailView.as_view(),
        name="sneaker"
    ),
    path(
        'sneakers/api/v1/',
        views.SneakerListViewHomeAPI.as_view(),
        name="sneaker_api_v1"
    ),
    path(
        'sneakers/api/v1/<int:pk>/',
        views.SneakerDetailAPI.as_view(),
        name="sneaker_api_v1_detail"
    ),
    path(
        'sneakers/theory/',
        views.theory,
        name="theory"
    ),
    path(
        'sneakers/api/v2/profile/<int:pk>/',
        views.profile_api_detail,
        name="sneaker_api_v2_profile"
    ),
    path(
        'sneakers/api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'sneakers/api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'sneakers/api/token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'
    ),
]

urlpatterns += sneaker_api_v2_router.urls
