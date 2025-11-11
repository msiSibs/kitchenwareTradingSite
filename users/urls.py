from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    
    # User Profile
    path('profile/', views.MyProfileDetailView.as_view(), name='my_profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='edit_profile'),
    path('<str:username>/', views.ProfileDetailView.as_view(), name='profile'),
    
    # Sellers
    path('sellers/', views.SellerListView.as_view(), name='seller_list'),
    path('sellers/<str:username>/', views.SellerDetailView.as_view(), name='seller_profile'),
]
