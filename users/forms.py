from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import UserProfile


class UserRegistrationForm(UserCreationForm):
    """Form for user registration with email validation."""
    
    email = forms.EmailField(
        required=True,
        help_text='Required. Enter a valid email address.',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address'
        })
    )
    first_name = forms.CharField(
        max_length=100,
        required=False,
        help_text='Optional.',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        required=False,
        help_text='Optional.',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'autofocus': True
            })
        }
    
    def __init__(self, *args, **kwargs):
        """Initialize form with Bootstrap styling."""
        super().__init__(*args, **kwargs)
        
        # Add Bootstrap classes to password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
        
        # Customize help texts
        self.fields['username'].help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        self.fields['password1'].help_text = 'At least 8 characters.'
        self.fields['password2'].help_text = 'Enter the same password as before.'
    
    def clean_email(self):
        """Validate that email is unique."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email address is already registered.')
        return email
    
    def clean_username(self):
        """Validate that username is unique."""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken.')
        return username
    
    def clean(self):
        """Validate form data."""
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match.')
        
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile."""
    
    bio = forms.CharField(
        label='Bio',
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Tell us about yourself (max 500 characters)',
            'maxlength': 500
        }),
        help_text='Short biography (optional, max 500 characters)'
    )
    
    phone_number = forms.CharField(
        label='Phone Number',
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+1 (555) 123-4567',
            'type': 'tel'
        }),
        help_text='Optional contact number'
    )
    
    profile_picture = forms.ImageField(
        label='Profile Picture',
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text='Upload a square image (recommended: 500x500px, max 5MB)'
    )
    
    remove_picture = forms.BooleanField(
        label='Remove profile picture',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        help_text='Check this box to remove your current profile picture'
    )
    
    is_seller = forms.BooleanField(
        label='I want to sell items',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        help_text='Check this box to enable selling on the marketplace'
    )
    
    class Meta:
        model = UserProfile
        fields = ['bio', 'phone_number', 'profile_picture', 'is_seller']
    
    def clean_phone_number(self):
        """Validate phone number format."""
        phone_number = self.cleaned_data.get('phone_number')
        
        if phone_number:
            # Remove common formatting characters
            cleaned = phone_number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+', '')
            
            # Check if it contains only digits
            if not cleaned.isdigit():
                raise ValidationError('Phone number should contain only digits and common formatting characters.')
            
            # Check length (7-15 digits is reasonable)
            if not (7 <= len(cleaned) <= 15):
                raise ValidationError('Phone number should be between 7 and 15 digits.')
        
        return phone_number
    
    def clean_profile_picture(self):
        """Validate profile picture."""
        profile_picture = self.cleaned_data.get('profile_picture')
        
        if profile_picture:
            # Check file size (5MB max)
            if profile_picture.size > 5 * 1024 * 1024:
                raise ValidationError('Profile picture must be less than 5MB.')
            
            # Check file type
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            file_extension = profile_picture.name.split('.')[-1].lower()
            
            if file_extension not in allowed_extensions:
                raise ValidationError(f'Only {", ".join(allowed_extensions).upper()} files are allowed.')
        
        return profile_picture


class UserUpdateForm(forms.ModelForm):
    """Form for updating user basic information (username, email, name)."""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address'
        })
    )
    
    first_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name'
        })
    )
    
    last_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name'
        })
    )
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
    
    def clean_email(self):
        """Validate that email is unique (except for current user)."""
        email = self.cleaned_data.get('email')
        user_id = self.instance.id
        
        if User.objects.filter(email=email).exclude(id=user_id).exists():
            raise ValidationError('This email address is already registered by another user.')
        
        return email
