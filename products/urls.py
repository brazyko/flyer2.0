from django.urls import path


from products.views import (
    product_detail_view,
    product_create_view,
    product_update_view,
    product_delete_view,
    ProductList,
    products_by_category,
    ProductLikeToggle,
    ProductLikeAPIToggle,
    )

app_name= 'products'
urlpatterns = [
    path('', ProductList, name='product-list1'),
    path('create/', product_create_view.as_view(), name='product-create'),
    path('<category_slug>/', products_by_category, name='product-categories'),
    path('<category_slug>/<prodcut_slug>/', product_detail_view.as_view(), name='product-detail'),
    path('<category_slug>/<prodcut_slug>/update/',product_update_view.as_view(), name='product-update'),   
    path('<category_slug>/<prodcut_slug>/delete/',product_delete_view.as_view(), name='product-delete'),
    path('<category_slug>/<prodcut_slug>/like', ProductLikeToggle.as_view(), name='like-toggle'),
    path('api/<category_slug>/<prodcut_slug>/like', ProductLikeAPIToggle.as_view(), name='like-api-toggle'),
]

