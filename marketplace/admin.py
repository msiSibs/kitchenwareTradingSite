from django.contrib import admin
from .models import Category, Item, ItemImage


class ItemImageInline(admin.TabularInline):
    """Inline admin for item images."""
    model = ItemImage
    extra = 1
    fields = ['image', 'is_primary']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin for Category model."""
    list_display = ['name', 'icon', 'item_count']
    search_fields = ['name', 'description']
    ordering = ['name']
    
    def item_count(self, obj):
        """Display count of items in category."""
        return obj.items.count()
    item_count.short_description = 'Items'


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Admin for Item model."""
    list_display = ['title', 'seller', 'category', 'price', 'condition', 'is_active', 'created_at']
    list_filter = ['is_active', 'condition', 'category', 'created_at']
    search_fields = ['title', 'description', 'seller__username']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ItemImageInline]
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'description', 'seller')
        }),
        ('Details', {
            'fields': ('category', 'condition', 'brand', 'material', 'price', 'location')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        queryset = super().get_queryset(request)
        return queryset.select_related('seller', 'category')


@admin.register(ItemImage)
class ItemImageAdmin(admin.ModelAdmin):
    """Admin for ItemImage model."""
    list_display = ['item', 'is_primary', 'uploaded_at']
    list_filter = ['is_primary', 'uploaded_at']
    search_fields = ['item__title']
    readonly_fields = ['uploaded_at']
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        queryset = super().get_queryset(request)
        return queryset.select_related('item')
