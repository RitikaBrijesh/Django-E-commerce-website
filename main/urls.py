from django.urls import path,include
from main import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns=[
    path('',views.Categories,name='categories'),
    path('brands/',views.brand_list,name='brands'),
    path('product_list/',views.product_list,name='product_list'),
    path('cat_productlist/<int:cat_id>',views.category_product_list,name='cat_productlist'),
    path('product_detail/<slug:slug>/<int:id>/',views.product_detail,name='product_detail'),
    path('brand_productlist/<int:brand_id>',views.brand_productList,name='brand_productlist'),
    path('search/',views.search,name='search'),
    path('API_details/',views.API_details.as_view(),name='API_details'),
    path('cart_list/<int:id>',views.cart_list,name='cart_list'),
    path('delete_product/<int:product_id>',views.delete_product,name='delete_product'),
    path('update_cart_item/<int:Product_id>',views.update_cart_item,name='update_cart_item'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns=format_suffix_patterns(urlpatterns)