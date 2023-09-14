from django.urls import path
from . import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('category/<str:category_name>/', views.category_products, name='category_products'),
    path('all_products/', views.products, name='products'),
    path('search/', views.search_products, name='search_products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('register/', views.register, name='register'),

]
