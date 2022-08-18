from django.urls import path

from . import views

app_name = 'authors'

urlpatterns = [
     path('register/', views.register_view, name='register'),
     path('register/create/', views.register_create, name='register_create'),
     path('login/', views.login_view, name='login'),
     path('login/create/', views.login_create, name='login_create'),
     path('logout/', views.logout_view, name='logout'),
     path('dashboard/', views.dashboard, name='dashboard'),
     path(
          'dashboard/sneaker/new/',
          views.dashboard_sneaker_new,
          name='dashboard_sneaker_new'
     ),
     path(
          'dashboard/sneaker/<int:id>/edit/',
          views.dashboard_sneaker_edit,
          name='dashboard_sneaker_edit'
     ),
]
