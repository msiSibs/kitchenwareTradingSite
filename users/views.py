from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q

from .models import UserProfile
from .forms import UserRegistrationForm, UserProfileForm


class RegisterView(CreateView):
    """User registration view - creates new user account."""
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    
    def form_valid(self, form):
        """Handle successful form submission."""
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Account created successfully! Please log in with your credentials."
        )
        return response


class UserLoginView(LoginView):
    """User login view - authenticates user."""
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('home')
    
    def get_success_url(self):
        """Redirect to next page or home."""
        next_page = self.request.GET.get('next')
        if next_page:
            return next_page
        return self.next_page
    
    def form_valid(self, form):
        """Handle successful login."""
        response = super().form_valid(form)
        messages.success(self.request, f"Welcome back, {self.request.user.username}!")
        return response


class UserLogoutView(LogoutView):
    """User logout view - logs out user and redirects to home."""
    next_page = reverse_lazy('home')
    
    def dispatch(self, request, *args, **kwargs):
        """Log out message and dispatch."""
        messages.success(request, "You have been logged out successfully.")
        return super().dispatch(request, *args, **kwargs)


class ProfileDetailView(DetailView):
    """Display user profile - public view."""
    model = UserProfile
    template_name = 'users/profile.html'
    context_object_name = 'profile'
    slug_field = 'user__username'
    slug_url_kwarg = 'username'
    
    def get_object(self, queryset=None):
        """Get profile by username."""
        username = self.kwargs.get('username')
        return get_object_or_404(UserProfile, user__username=username)
    
    def get_context_data(self, **kwargs):
        """Add additional context data."""
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        
        # Add seller info if applicable
        context['is_profile_owner'] = self.request.user == profile.user
        
        # Add seller's items if they are a seller
        if profile.is_seller:
            from marketplace.models import Item
            context['seller_items'] = Item.objects.filter(
                seller=profile.user,
                is_active=True
            ).select_related('category').prefetch_related('images')[:6]
        
        return context


class MyProfileDetailView(LoginRequiredMixin, DetailView):
    """Display current user's own profile."""
    model = UserProfile
    template_name = 'users/my_profile.html'
    context_object_name = 'profile'
    
    def get_object(self, queryset=None):
        """Get current user's profile."""
        return self.request.user.profile
    
    def get_context_data(self, **kwargs):
        """Add additional context data."""
        context = super().get_context_data(**kwargs)
        
        # Add seller info if applicable
        if self.object.is_seller:
            from marketplace.models import Item
            context['seller_items'] = Item.objects.filter(
                seller=self.request.user,
                is_active=True
            ).select_related('category').prefetch_related('images')
        
        return context


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edit user profile - only user can edit their own profile."""
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'users/edit_profile.html'
    context_object_name = 'profile'
    success_url = reverse_lazy('users:my_profile')
    
    def get_object(self, queryset=None):
        """Get current user's profile."""
        return self.request.user.profile
    
    def test_func(self):
        """Check if user owns the profile."""
        return self.get_object().user == self.request.user
    
    def form_valid(self, form):
        """Handle successful form submission."""
        # Check if user wants to remove profile picture
        if form.cleaned_data.get('remove_picture') and self.object.profile_picture:
            # Delete the image file from storage
            self.object.profile_picture.delete(save=False)
            # Clear the profile_picture field
            self.object.profile_picture = None
            self.object.save()
            messages.info(self.request, "Profile picture removed successfully!")
        
        response = super().form_valid(form)
        messages.success(self.request, "Profile updated successfully!")
        return response
    
    def handle_no_permission(self):
        """Handle permission denied."""
        messages.error(self.request, "You don't have permission to edit this profile.")
        return redirect('home')


class SellerListView(ListView):
    """List all verified sellers."""
    model = UserProfile
    template_name = 'users/seller_list.html'
    context_object_name = 'sellers'
    paginate_by = 12
    
    def get_queryset(self):
        """Get verified sellers ordered by rating."""
        return UserProfile.objects.filter(
            is_seller=True,
            verification_status='verified'
        ).order_by('-average_rating')
    
    def get_context_data(self, **kwargs):
        """Add context data."""
        context = super().get_context_data(**kwargs)
        context['total_sellers'] = self.get_queryset().count()
        return context


class SellerDetailView(DetailView):
    """Display seller profile with items."""
    model = UserProfile
    template_name = 'users/seller_profile.html'
    context_object_name = 'profile'
    slug_field = 'user__username'
    slug_url_kwarg = 'username'
    
    def get_queryset(self):
        """Only show verified sellers."""
        return UserProfile.objects.filter(
            is_seller=True,
            verification_status='verified'
        )
    
    def get_object(self, queryset=None):
        """Get profile by username."""
        username = self.kwargs.get('username')
        return get_object_or_404(self.get_queryset(), user__username=username)
    
    def get_context_data(self, **kwargs):
        """Add seller's items."""
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        
        # Get seller's active items
        from marketplace.models import Item
        context['seller_items'] = Item.objects.filter(
            seller=profile.user,
            is_active=True
        ).select_related('category').prefetch_related('images').order_by('-created_at')
        
        return context
