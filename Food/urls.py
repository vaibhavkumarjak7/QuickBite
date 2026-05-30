from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"items",views.ItemViewSet,basename='item')

app_name = 'Food'
urlpatterns = [
    path("api/",include(router.urls)),
    # path('api/items/',views.item_list_api,name='item_list_api'),
    # path("api/items/<int:pk>/",views.item_detail_api,name='item_detail_api'),
    # /food/
    path('',views.index,name='index'),
    # /food/1
    path('<int:pk>/',views.FoodDetail.as_view(),name='detail'),
    path('add/',views.create_item,name='create_item'),
    path('update/<int:pk>/',views.ItemUpdateView.as_view(),name='update_item'),
    path('delete/<int:pk>/',views.ItemDelete.as_view(),name='delete_item'),
]
