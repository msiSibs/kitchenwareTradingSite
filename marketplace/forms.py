from django import forms
from .models import Item, ItemImage


class ItemCreationForm(forms.ModelForm):
    """Form for creating and editing marketplace items."""
    
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Item title'
        }),
        help_text='Brief title for your item (max 200 characters)'
    )
    
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Describe your item in detail...'
        }),
        help_text='Detailed description including condition, dimensions, features, etc.'
    )
    
    category = forms.ModelChoiceField(
        queryset=None,  # Will be set in __init__
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        help_text='Select a category for your item'
    )
    
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'step': '0.01',
            'min': '0'
        }),
        help_text='Price in dollars (e.g., 29.99)'
    )
    
    condition = forms.ChoiceField(
        choices=Item.CONDITION_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        help_text='Select item condition'
    )
    
    brand = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., KitchenAid, Le Creuset'
        }),
        help_text='Brand/manufacturer (optional)'
    )
    
    material = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Stainless Steel, Cast Iron'
        }),
        help_text='Primary material (optional)'
    )
    
    location = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'City, State or general location'
        }),
        help_text='Where the item is located for pickup/delivery'
    )
    
    class Meta:
        model = Item
        fields = ['title', 'description', 'category', 'price', 'condition', 'brand', 'material', 'location']
    
    def __init__(self, *args, **kwargs):
        """Initialize form and set category queryset."""
        super().__init__(*args, **kwargs)
        # Set category queryset to all categories ordered by name
        from .models import Category
        self.fields['category'].queryset = Category.objects.all().order_by('name')


class ItemImageForm(forms.ModelForm):
    """Form for uploading item images."""
    
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text='Upload an image (recommended: 500x500px or larger, max 5MB)'
    )
    
    is_primary = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        help_text='Set as primary/thumbnail image?'
    )
    
    class Meta:
        model = ItemImage
        fields = ['image', 'is_primary']
    
    def clean_image(self):
        """Validate image file."""
        image = self.cleaned_data.get('image')
        
        if image:
            # Check file size (5MB max)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Image must be less than 5MB.')
            
            # Check file type
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            file_extension = image.name.split('.')[-1].lower()
            
            if file_extension not in allowed_extensions:
                raise forms.ValidationError(
                    f'Only {", ".join(allowed_extensions).upper()} files are allowed.'
                )
        
        return image
