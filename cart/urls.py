from django.urls import path
from . import views
app_name="cart"


urlpatterns=[
    path("add_cart/<int:p>",views.add_cart,name="add_cart"),
    path("cartview/",views.cartview,name="cartview"),
    path("itemless/<int:id>",views.cart_item_less,name="item_less"),
    path("cartremove/<int:id>",views.cart_remove,name="cart_remove"),
    path("orderform",views.orderform,name="orderform"),
path('add_review/<int:order_id>/', views.add_review, name='add_review'),
path('product/<int:product_id>/reviews/', views.display_all_review, name='display_all_review'),
]
