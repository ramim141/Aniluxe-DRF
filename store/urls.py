from django.urls import path, include
from . import views




urlpatterns = [
    # Category URLs
 
    path('categories/', views.get_categories, name='get_categories'),

    # Product URLs
    path('products/', views.get_products, name='get_products'),
    path('products/<int:pk>/', views.get_product, name='get_product'),

    # Cart URLs
    path('cart/', views.get_cart, name='get_cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),

    # Wishlist URLs
    path('wishlist/', views.get_wishlist, name='get_wishlist'),
    path('wishlist/add/', views.add_to_wishlist, name='add_to_wishlist'),

    # Order URLs
    path('orders/', views.get_orders, name='get_orders'),
    path('order/place/', views.place_order, name='place_order'),

    # Review URLs
    path('reviews/add/', views.add_review, name='add_review'),
]
