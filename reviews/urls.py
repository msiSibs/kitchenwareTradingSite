from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('create/<int:item_id>/', views.create_review_view, name='create'),
    path('<int:pk>/', views.review_detail_view, name='detail'),
    path('<int:pk>/delete/', views.review_delete_view, name='delete'),
]
