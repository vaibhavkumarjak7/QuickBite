from django.urls import path
from . import views

app_name = 'Food'
urlpatterns = [
    path('items-api/',views.item_list_api,name='item_list_api'),
    path("api/items/<int:pk>",views.item_detail_api,name='item_detail_api'),
    # /food/
    path('',views.index,name='index'),
    # /food/1
    path('<int:pk>/',views.FoodDetail.as_view(),name='detail'),
    path('add/',views.create_item,name='create_item'),
    path('update/<int:pk>/',views.ItemUpdateView.as_view(),name='update_item'),
    path('delete/<int:pk>/',views.ItemDelete.as_view(),name='delete_item'),
]
