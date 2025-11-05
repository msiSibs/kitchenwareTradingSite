from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.item_list_view, name='list'),
    path('create/', views.item_create_view, name='create'),
    path('<int:pk>/', views.item_detail_view, name='detail'),
    path('<int:pk>/edit/', views.item_edit_view, name='edit'),
    path('<int:pk>/delete/', views.item_delete_view, name='delete'),
]
