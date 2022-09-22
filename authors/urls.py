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
          views.DashboardSneaker.as_view(),
          name='dashboard_sneaker_new'
     ),
     path(
          'dashboard/sneaker/delete/',
          views.DashboardSneakerDelete.as_view(),
          name='dashboard_sneaker_delete'
     ),
     path(
          'dashboard/sneaker/<int:id>/edit/',
          views.DashboardSneaker.as_view(),
          name='dashboard_sneaker_edit'
     ),
     path(
          'profile/<int:id>/',
          views.ProfileView.as_view(),
          name='profile'
     ),
]
