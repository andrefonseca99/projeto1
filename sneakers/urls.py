from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('sneakers/<int:id>/', views.sneaker)
]
