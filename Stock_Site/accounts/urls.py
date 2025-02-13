from django.urls import path
from . import views

urlpatterns = [
    path('', views.home1, name='home1'),
    path('home2/', views.home2, name='home2'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('calculators/', views.calculators, name='calculators'), 
    path('dashboard/', views.dashboard, name='dashboard'),
    path('stocks/<str:stock_symbol>/', views.stock_detail, name='stock_detail'),
    path('add_to_watchlist/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove-from-watchlist/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('fetch-live-price/', views.fetch_live_stock_price, name='fetch_live_price'),
    path('profile/', views.profile, name='profile'),
    path("search/", views.search_stocks, name="search_stocks"),
    path('admin/', views.admin, name='admin'),
]