from django.urls import path

from sneakers import views

# sneakers:sneaker
app_name = 'sneakers'

urlpatterns = [
    path('', views.SneakerListViewHome.as_view(), name="home"),
    path('sneakers/search/', views.SneakerListViewSearch.as_view(), name="search"),  # noqa: E501
    path('sneakers/category/<int:category_id>/', views.SneakerListViewCategory.as_view(), name="category"),  # noqa: E501
    path('sneakers/<int:pk>/', views.SneakerDetailView.as_view(), name="sneaker"),  # noqa: E501
    path('sneakers/api/v1/', views.SneakerListViewHomeAPI.as_view(), name="sneaker_api_v1"),  # noqa: E501
    path('sneakers/api/v1/<int:pk>/', views.SneakerDetailAPI.as_view(), name="sneaker_api_v1_detail"),  # noqa: E501
    path('sneakers/theory/', views.theory, name="theory"),
    path('sneakers/api/v2/', views.sneaker_api_list, name="sneaker_api_v2"),
]
