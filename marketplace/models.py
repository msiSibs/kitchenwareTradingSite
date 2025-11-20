from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Product category for marketplace items."""
    name = models.CharField(max_length=100, unique=True, help_text="Category name")
    description = models.TextField(blank=True, help_text="Category description")
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon name (e.g., 'fa-utensils')")
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Item(models.Model):
    """Marketplace item listing."""
    CONDITION_CHOICES = [
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('needs_repair', 'Needs Repair'),
    ]
    
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items', help_text="Item seller")
    title = models.CharField(max_length=200, help_text="Item title")
    description = models.TextField(help_text="Detailed item description")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='items', help_text="Item category")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Item price")
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, help_text="Item condition")
    brand = models.CharField(max_length=100, blank=True, help_text="Brand/manufacturer name")
    material = models.CharField(max_length=100, blank=True, help_text="Primary material")
    location = models.CharField(max_length=200, help_text="Pickup/delivery location")
    is_active = models.BooleanField(default=True, help_text="Is item currently available for sale?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        indexes = [
            models.Index(fields=['seller', '-created_at']),
            models.Index(fields=['category', 'is_active']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_primary_image(self):
        """Get primary image for item or first image if none marked."""
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary
        return self.images.first()


class ItemImage(models.Model):
    """Image for marketplace item (supports multiple images per item)."""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images', help_text="Associated item")
    image = models.ImageField(upload_to='listings/%Y/%m/%d/', help_text="Item image")
    is_primary = models.BooleanField(default=False, help_text="Use as primary display image?")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary', 'uploaded_at']
        verbose_name = 'Item Image'
        verbose_name_plural = 'Item Images'
    
    def __str__(self):
        return f"Image for {self.item.title}"
