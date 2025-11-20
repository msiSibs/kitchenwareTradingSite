from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Item, Category, ItemImage
from .forms import ItemCreationForm, ItemImageForm


class ItemListView(ListView):
    """Display all active marketplace items with pagination."""
    model = Item
    template_name = 'marketplace/listing_list.html'
    context_object_name = 'items'
    paginate_by = 12
    
    def get_queryset(self):
        """Filter for active items and optimize with select_related."""
        queryset = Item.objects.filter(is_active=True).select_related(
            'seller', 'category'
        ).prefetch_related('images')
        
        # Filter by category if provided
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Add categories to context."""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by('name')
        context['selected_category'] = self.request.GET.get('category')
        return context


class ItemDetailView(DetailView):
    """Display detailed view of a single item with images and seller info."""
    model = Item
    template_name = 'marketplace/listing_detail.html'
    context_object_name = 'item'
    
    def get_queryset(self):
        """Only show active items."""
        return Item.objects.filter(is_active=True).select_related(
            'seller', 'seller__profile', 'category'
        ).prefetch_related('images')
    
    def get_context_data(self, **kwargs):
        """Add images and seller profile to context."""
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.images.all()
        context['primary_image'] = self.object.get_primary_image()
        return context


class ItemCreateView(LoginRequiredMixin, CreateView):
    """Create a new marketplace item."""
    model = Item
    form_class = ItemCreationForm
    template_name = 'marketplace/listing_create.html'
    
    def dispatch(self, request, *args, **kwargs):
        """Check if user is a seller before allowing listing creation."""
        if not request.user.is_authenticated:
            return redirect('users:login')
        if not request.user.profile.is_seller:
            messages.warning(request, "You must be registered as a seller to create listings. Please update your profile.")
            return redirect('users:edit_profile')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """Set seller to current user and handle image uploads."""
        form.instance.seller = self.request.user
        response = super().form_valid(form)
        
        # Handle image uploads
        images = self.request.FILES.getlist('images')
        is_primary = True
        for image_file in images:
            ItemImage.objects.create(
                item=self.object,
                image=image_file,
                is_primary=is_primary
            )
            is_primary = False
        
        messages.success(self.request, "Item created successfully!")
        return response
    
    def get_success_url(self):
        """Redirect to newly created item detail."""
        return reverse_lazy('marketplace:detail', kwargs={'pk': self.object.pk})


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edit an existing marketplace item (seller only)."""
    model = Item
    form_class = ItemCreationForm
    template_name = 'marketplace/listing_edit.html'
    
    def test_func(self):
        """Check if user is the item seller and is registered as seller."""
        item = self.get_object()
        return item.seller == self.request.user and self.request.user.profile.is_seller
    
    def get_context_data(self, **kwargs):
        """Add existing images to context."""
        context = super().get_context_data(**kwargs)
        context['existing_images'] = self.object.images.all()
        return context
    
    def form_valid(self, form):
        """Handle successful form submission and image uploads."""
        response = super().form_valid(form)
        
        # Handle new image uploads
        images = self.request.FILES.getlist('images')
        if images:
            # If adding new images and no primary image exists, set first as primary
            has_primary = self.object.images.filter(is_primary=True).exists()
            is_primary = not has_primary
            
            for image_file in images:
                ItemImage.objects.create(
                    item=self.object,
                    image=image_file,
                    is_primary=is_primary
                )
                is_primary = False
        
        messages.success(self.request, "Item updated successfully!")
        return response
    
    def get_success_url(self):
        """Redirect to item detail."""
        return reverse_lazy('marketplace:detail', kwargs={'pk': self.object.pk})
    
    def handle_no_permission(self):
        """Handle permission denied."""
        messages.error(self.request, "You don't have permission to edit this item.")
        return redirect('marketplace:detail', pk=self.get_object().pk)


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Soft delete a marketplace item (seller only)."""
    model = Item
    template_name = 'marketplace/listing_confirm_delete.html'
    success_url = reverse_lazy('marketplace:list')
    
    def test_func(self):
        """Check if user is the item seller and is registered as seller."""
        item = self.get_object()
        return item.seller == self.request.user and self.request.user.profile.is_seller
    
    def form_valid(self, form):
        """Override to do soft delete instead of hard delete."""
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        messages.success(self.request, "Item has been removed from marketplace.")
        return redirect(self.success_url)
    
    def handle_no_permission(self):
        """Handle permission denied."""
        messages.error(self.request, "You don't have permission to delete this item.")
        return redirect('marketplace:detail', pk=self.get_object().pk)
