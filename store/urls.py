from django.urls import path
from  .import  views


urlpatterns = [
    path('',views.getProducts,name="products"),
    path('<str:pk>/reviews/',views.createProductReview,name="create-review"),
    path('top/',views.getTopProducts,name="top-products"),
    path('<str:pk>/',views.getProduct,name="product"),
    
    path('add/',views.addOrderItems,name="orders-add"),
    path('myorders/',views.getMyOrders,name="myorders"),
    path('<str:pk>/',views.getOrderById,name="user-order"),
    path('<str:pk>/pay/',views.updateOrderToPaid,name="pay"),
]