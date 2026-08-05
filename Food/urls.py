from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r"items",views.ItemViewSet,basename='item')
router.register(r"orders",views.OrderViewSet,basename='order')

app_name = 'Food'
urlpatterns = [
    path("api/token/",TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path("api/token/refresh/",TokenRefreshView.as_view(),name='token_refresh'),
    path("api/",include(router.urls)),
    # path('api/items/',views.item_list_api,name='item_list_api'),
    # path("api/items/<int:pk>/",views.item_detail_api,name='item_detail_api'),
    # /food/
    path('',views.index,name='index'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='order_history'),
    # /food/1
    path('<int:pk>/',views.FoodDetail.as_view(),name='detail'),
    path('add/',views.create_item,name='create_item'),
    path('update/<int:pk>/',views.ItemUpdateView.as_view(),name='update_item'),
    path('delete/<int:pk>/',views.ItemDelete.as_view(),name='delete_item'),
]
