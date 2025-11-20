from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    # Listing views
    path('', views.ItemListView.as_view(), name='list'),
    path('create/', views.ItemCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ItemDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ItemUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.ItemDeleteView.as_view(), name='delete'),
]
