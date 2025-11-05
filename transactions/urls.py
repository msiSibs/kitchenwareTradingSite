from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('', views.transaction_list_view, name='list'),
    path('<int:pk>/', views.transaction_detail_view, name='detail'),
    path('create/', views.transaction_create_view, name='create'),
]
