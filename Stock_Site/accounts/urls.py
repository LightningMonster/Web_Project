from django.urls import path
from . import views

urlpatterns = [
    path('', views.home1, name='home1'),
    path('home2/', views.home2, name='home2'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('calculators/', views.calculators, name='calculators'),
    path('nse/', views.nse_stocks, name='nse'),
    path('bse/', views.bse_stocks, name='bse'),

]