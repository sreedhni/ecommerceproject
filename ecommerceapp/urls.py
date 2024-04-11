from django.urls import path
from ecommerceapp import views
app_name="ecommerceapp"

urlpatterns = [
    path("",views.index,name='index'),
    path("contact",views.contact,name='contact'),
    path("about",views.about,name='about'),
    path('add-category/', views.add_category, name='add_category'),
    path('categories/', views.category_list, name='category_list'),
    path('add_product/', views.add_product, name='add_product'),
    path('products/',views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/edit/',views.edit_product, name='product_edit'),
    path('product/<int:pk>/delete/',views.ProductDeleteView.as_view(), name='product_delete'),
    path('all-orders/<int:pk>/',views.all_customers,name="all-orders"),
    path('manage-orders/',views.manage_orders,name="manage-orders"),
    path('orderd-product/', views.orders_pro, name='orderd-product'),
    path('change-status/<int:order_id>/<str:new_status>/',views.change_applicant_status, name='change-status')




]
