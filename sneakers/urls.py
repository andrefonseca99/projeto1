from django.urls import path

from . import views

# sneakers:sneaker
app_name = 'sneakers'

urlpatterns = [
    path('', views.home, name="home"),
    path('sneakers/category/<int:category_id>/', views.category, name="category"),
    path('sneakers/<int:id>/', views.sneaker, name="sneaker"),
    
]
