from django.urls import path

from . import views

# sneakers:sneaker
app_name = 'sneakers'

urlpatterns = [
    path('', views.SneakerListViewHome.as_view(), name="home"),
    path('sneakers/search/', views.SneakerListViewSearch.as_view(), name="search"),  # noqa: E501
    path('sneakers/category/<int:category_id>/', views.SneakerListViewCategory.as_view(), name="category"),  # noqa: E501
    path('sneakers/<int:pk>/', views.SneakerDetailView.as_view(), name="sneaker"),  # noqa: E501
]
