# Kitchenware Marketplace - Development Plan

This document provides a detailed implementation roadmap with specific tasks, models, views, and deliverables for each development phase.

---

## Phase 1: Project Setup & Initialization

**Duration**: 1-2 days  
**Priority**: 🔴 Critical  
**Status**: ✅ Complete (November 6, 2025)

### Overview
Establish the Django project foundation with core configuration, database setup, and basic templates.

### Key Tasks
- [x] Initialize Django project and create apps
- [x] Configure database (PostgreSQL)
- [x] Set up environment variables and `.env` file
- [x] Configure static files and media handling
- [x] Create base templates and CSS structure
- [x] Set up Git repository and `.gitignore`

### Files to Create/Modify
```
NEW:
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── core/
│   ├── templates/base.html
│   ├── templates/navbar.html
│   ├── static/css/main.css
│   └── static/js/main.js
└── media/ (directory)
```

### Example Code

**`requirements.txt`**:
```
Django==4.2.7
psycopg2-binary==2.9.9
python-dotenv==1.0.0
Pillow==10.1.0
django-crispy-forms==2.1
crispy-bootstrap5==0.7
```

**`config/settings.py` (key sections)**:
```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party
    'crispy_forms',
    'crispy_bootstrap5',
    
    # Local
    'core',
    'users',
    'marketplace',
    'messaging',
    'transactions',
    'reviews',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'kitchenware_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

### Deliverables
✅ Functional Django project structure  
✅ Database connected and tested  
✅ Base templates and styling in place  
✅ Environment configuration complete  

---

## Phase 2: User Authentication & Profiles

**Duration**: 2-3 days  
**Priority**: 🔴 Critical  
**Status**: ✅ Complete (November 11, 2025)
**Depends On**: Phase 1

### Overview
Implement user registration, login, and profile management with seller capabilities.

### Key Tasks
- [x] Create `UserProfile` model with seller fields
- [x] Implement user registration with email validation
- [x] Build secure login/logout functionality
- [x] Create user profile pages (own and public seller profiles)
- [x] Add profile editing functionality
- [x] Create comprehensive test suite (36 tests - ALL PASSING)

### Models to Create

**`users/models.py`**:
```python
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, max_length=500)
    profile_picture = models.ImageField(upload_to='profiles/%Y/%m/%d/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    is_seller = models.BooleanField(default=False)
    verification_status = models.CharField(
        max_length=20,
        choices=[('unverified', 'Unverified'), ('verified', 'Verified')],
        default='unverified'
    )
    total_sales = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
```

### Views to Create

**`users/views.py`**:
```python
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile
from .forms import UserRegistrationForm, UserProfileForm

class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = '/login/'

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

class UserLogoutView(LogoutView):
    next_page = '/'

class ProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'users/profile.html'
    context_object_name = 'profile'

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'users/edit_profile.html'
    success_url = '/profile/'
```

### Forms to Create

**`users/forms.py`**:
```python
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture', 'phone_number', 'is_seller']
```

### Templates to Create
- `users/register.html` - Registration form
- `users/login.html` - Login form
- `users/profile.html` - User profile display
- `users/edit_profile.html` - Profile editing form
- `users/seller_profile.html` - Public seller profile

### Database Migrations
```bash
python manage.py makemigrations users
python manage.py migrate users
```

### Deliverables
✅ User registration with email/username validation  
✅ Secure login/logout system with messages  
✅ User profile model with seller capabilities  
✅ Profile viewing (own and public profiles)  
✅ Profile editing with image upload  
✅ Seller directory and verification system  
✅ Comprehensive test suite (36 tests - ALL PASSING)  
✅ Auto-profile creation via signals  
✅ Bootstrap 5 responsive design for all forms  

### Known Limitations / Future Enhancements
- ⚠️ **Profile Picture Removal**: Users currently cannot remove uploaded profile pictures
- ⚠️ **Image Cleanup**: Uploaded images should have deletion functionality and cleanup on user profile deletion
- 📝 **TODO**: Add profile picture removal button and implement cascade deletion

---

## Phase 3: Core Marketplace - Listings CRUD

**Duration**: 3-4 days  
**Priority**: 🔴 Critical  
**Status**: Not Started  
**Depends On**: Phase 1, Phase 2

### Overview
Build item listing functionality with full CRUD operations and image handling.

### Key Tasks
- [ ] Create `Category` and `Item` models
- [ ] Implement `ItemImage` model for multiple images
- [ ] Build listing creation view with image upload
- [ ] Create listing detail and list views
- [ ] Implement listing editing (sellers only)
- [ ] Add soft delete functionality
- [ ] Create seller dashboard

### Models to Create

**`marketplace/models.py`**:
```python
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Item(models.Model):
    CONDITION_CHOICES = [
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('needs_repair', 'Needs Repair'),
    ]
    
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    brand = models.CharField(max_length=100, blank=True)
    material = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['seller', '-created_at']),
            models.Index(fields=['category', 'is_active']),
        ]
    
    def __str__(self):
        return self.title

class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listings/%Y/%m/%d/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary', 'uploaded_at']
```

### Views to Create

**`marketplace/views.py`**:
```python
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from .models import Item, Category, ItemImage
from .forms import ItemCreationForm, ItemImageForm

class ItemListView(ListView):
    model = Item
    template_name = 'marketplace/listing_list.html'
    context_object_name = 'items'
    paginate_by = 12
    
    def get_queryset(self):
        return Item.objects.filter(is_active=True).select_related('seller', 'category')

class ItemDetailView(DetailView):
    model = Item
    template_name = 'marketplace/listing_detail.html'
    context_object_name = 'item'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.images.all()
        return context

class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemCreationForm
    template_name = 'marketplace/listing_create.html'
    success_url = '/marketplace/'
    
    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    form_class = ItemCreationForm
    template_name = 'marketplace/listing_edit.html'
    
    def test_func(self):
        item = self.get_object()
        return item.seller == self.request.user

class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    success_url = '/marketplace/'
    
    def test_func(self):
        item = self.get_object()
        return item.seller == self.request.user
```

### Forms to Create

**`marketplace/forms.py`**:
```python
from django import forms
from .models import Item, ItemImage

class ItemCreationForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'category', 'price', 
                  'condition', 'brand', 'material', 'location']

class ItemImageForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        fields = ['image']
```

### Templates to Create
- `marketplace/index.html` - Homepage
- `marketplace/listing_list.html` - All items list
- `marketplace/listing_detail.html` - Item detail page
- `marketplace/listing_create.html` - Create listing form
- `marketplace/listing_edit.html` - Edit listing form

### Deliverables
✅ Item model with complete fields  
✅ Multiple image support per item  
✅ Full CRUD operations for items  
✅ Listing creation with images  
✅ Seller-only edit/delete capabilities  

---

## Phase 4: Search & Filtering

**Duration**: 2 days  
**Priority**: 🟠 High  
**Status**: Not Started  
**Depends On**: Phase 3

### Overview
Enable users to discover items through advanced search and filtering.

### Key Tasks
- [ ] Install django-filter package
- [ ] Create `ItemFilter` class with all search parameters
- [ ] Implement filtered list view
- [ ] Build filter UI in template
- [ ] Add search bar to navbar
- [ ] Optimize database queries with select_related

### Implementation

**`marketplace/filters.py`**:
```python
import django_filters
from django.db.models import Q
from .models import Item, Category

class ItemFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Search title'
    )
    price_min = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        label='Min Price'
    )
    price_max = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        label='Max Price'
    )
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all()
    )
    condition = django_filters.ChoiceFilter(
        choices=Item.CONDITION_CHOICES
    )
    location = django_filters.CharFilter(
        field_name='location',
        lookup_expr='icontains'
    )
    
    class Meta:
        model = Item
        fields = ['category', 'condition']

class ItemSearchView(ListView):
    model = Item
    template_name = 'marketplace/search_results.html'
    context_object_name = 'items'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Item.objects.filter(is_active=True)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query)
            )
        return queryset
```

### URL Configuration

**`marketplace/urls.py`**:
```python
from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.ItemListView.as_view(), name='list'),
    path('search/', views.ItemSearchView.as_view(), name='search'),
    path('item/<int:pk>/', views.ItemDetailView.as_view(), name='detail'),
    path('create/', views.ItemCreateView.as_view(), name='create'),
    path('item/<int:pk>/edit/', views.ItemUpdateView.as_view(), name='edit'),
    path('item/<int:pk>/delete/', views.ItemDeleteView.as_view(), name='delete'),
]
```

### Deliverables
✅ Advanced filtering functionality  
✅ Full-text search implementation  
✅ Optimized database queries  
✅ Filter UI in templates  

---

## Phase 5: Messaging System

**Duration**: 2-3 days  
**Priority**: 🟠 High  
**Status**: Not Started  
**Depends On**: Phase 2, Phase 3

### Overview
Enable direct messaging between buyers and sellers.

### Key Tasks
- [ ] Create `Conversation` and `Message` models
- [ ] Build conversation creation from item detail page
- [ ] Implement inbox view
- [ ] Build conversation thread display
- [ ] Add message sending functionality
- [ ] Implement message read status

### Models to Create

**`messaging/models.py`**:
```python
from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    item = models.ForeignKey('marketplace.Item', on_delete=models.SET_NULL, 
                            null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Conversation {self.id}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE,
                                    related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
```

### Views to Create

**`messaging/views.py`**:
```python
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .models import Conversation, Message
from .forms import MessageForm

class InboxView(LoginRequiredMixin, ListView):
    model = Conversation
    template_name = 'messaging/inbox.html'
    context_object_name = 'conversations'
    
    def get_queryset(self):
        return self.request.user.conversations.all().prefetch_related('participants', 'messages')

class ConversationDetailView(LoginRequiredMixin, DetailView):
    model = Conversation
    template_name = 'messaging/conversation.html'
    context_object_name = 'conversation'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = self.object.messages.all()
        return context

class SendMessageView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'messaging/send_message.html'
    
    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.conversation_id = self.kwargs['conversation_id']
        return super().form_valid(form)
```

### Deliverables
✅ Conversation and message models  
✅ Inbox functionality  
✅ Message thread display  
✅ Real-time message sending  

---

## Phase 6: Transactions & Purchase Tracking

**Duration**: 2 days  
**Priority**: 🟠 High  
**Status**: Not Started  
**Depends On**: Phase 3

### Overview
Track purchase history and transaction status.

### Key Tasks
- [ ] Create `Transaction` model with status tracking
- [ ] Implement checkout process
- [ ] Build transaction history view
- [ ] Add transaction detail pages
- [ ] Implement status workflow (pending → confirmed → completed)

### Models to Create

**`transactions/models.py`**:
```python
from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, 
                             related_name='purchases')
    seller = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='sales')
    item = models.ForeignKey('marketplace.Item', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, 
                             default='pending')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Transaction {self.id} - {self.item.title}"
```

### Views to Create

**`transactions/views.py`**:
```python
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction

class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 20
    
    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(
            models.Q(buyer=user) | models.Q(seller=user)
        ).select_related('buyer', 'seller', 'item')

class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = 'transactions/transaction_detail.html'
    context_object_name = 'transaction'
```

### Deliverables
✅ Transaction model with status tracking  
✅ Transaction history views  
✅ Status workflow implementation  

---

## Phase 7: Reviews & Rating System

**Duration**: 1-2 days  
**Priority**: 🟡 Medium  
**Status**: Not Started  
**Depends On**: Phase 6

### Overview
Build trust through user ratings and reviews.

### Key Tasks
- [ ] Create `Review` model linked to transactions
- [ ] Implement 1-5 star rating system
- [ ] Build review creation form
- [ ] Display reviews on seller profiles
- [ ] Calculate average ratings

### Models to Create

**`reviews/models.py`**:
```python
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, 
                                related_name='given_reviews')
    reviewed_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                     related_name='received_reviews')
    transaction = models.OneToOneField('transactions.Transaction', 
                                       on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('reviewer', 'reviewed_user', 'transaction')
```

### Deliverables
✅ Review and rating models  
✅ Review creation functionality  
✅ Ratings display on profiles  

---

## Phase 8: Admin Dashboard & Moderation

**Duration**: 1-2 days  
**Priority**: 🟡 Medium  
**Status**: Not Started  
**Depends On**: Phase 3, 6, 7

### Overview
Provide administrative tools for site management.

### Key Tasks
- [ ] Register all models in Django admin
- [ ] Create custom admin views for moderation
- [ ] Add list filters and search
- [ ] Implement user suspension capability
- [ ] Create admin statistics dashboard

### Implementation

**`marketplace/admin.py`**:
```python
from django.contrib import admin
from .models import Item, Category, ItemImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'price', 'created_at', 'is_active']
    list_filter = ['created_at', 'condition', 'is_active', 'category']
    search_fields = ['title', 'seller__username', 'seller__email']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['activate_items', 'deactivate_items']
    
    def activate_items(self, request, queryset):
        queryset.update(is_active=True)
    
    def deactivate_items(self, request, queryset):
        queryset.update(is_active=False)
```

### Deliverables
✅ Admin interface for all models  
✅ Custom actions for bulk operations  
✅ Search and filtering capabilities  

---

## Phase 9: Frontend Polish & Deployment

**Duration**: 2-3 days  
**Priority**: 🟡 Medium  
**Status**: Not Started  
**Depends On**: All previous phases

### Overview
Refine UI/UX and prepare for production.

### Key Tasks
- [ ] Implement responsive design with Bootstrap
- [ ] Add AJAX features for better UX
- [ ] Optimize static files
- [ ] Create error pages (404, 500)
- [ ] Implement pagination across all list views
- [ ] Add breadcrumbs and improved navigation
- [ ] Configure production settings
- [ ] Test security settings

### Templates to Create/Modify
- Enhanced `core/templates/base.html` with Bootstrap
- `core/templates/404.html` - Not found page
- `core/templates/500.html` - Server error page
- Add pagination to all list views

### Production Checklist
- [ ] `DEBUG = False` in settings
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up `SECRET_KEY` from environment
- [ ] Configure CSRF and security middleware
- [ ] Set up email backend for notifications
- [ ] Configure CORS headers if using API
- [ ] Use WhiteNoise for static files

### Deliverables
✅ Responsive and polished UI  
✅ Production-ready configuration  
✅ Error handling pages  

---

## Optional/Advanced Phases

### Phase 10: Notifications System
**Duration**: 2-3 days | **Priority**: 🟡 Medium

- Email notifications for messages
- In-app notification bell
- User notification preferences
- Tools: Celery, Redis, django-notifications

### Phase 11: Advanced Search
**Duration**: 2-3 days | **Priority**: 🟡 Medium

- Elasticsearch integration
- Full-text search
- Saved searches and alerts
- Tools: Elasticsearch

### Phase 12: Payment Integration
**Duration**: 2-3 days | **Priority**: 🟠 High

- Stripe payment processing
- Multiple payment methods
- Invoice generation
- Tools: stripe-django

### Phase 13: Analytics
**Duration**: 1-2 days | **Priority**: 🟡 Medium

- Marketplace statistics dashboard
- Seller performance metrics
- Tools: Django Q, Celery Beat

### Phase 14: Mobile App Support
**Duration**: 3-5 days | **Priority**: 🟡 Medium

- Django REST Framework API
- Token-based authentication
- API documentation
- Tools: DRF, drf-spectacular

### Phase 15: Advanced Admin
**Duration**: 1-2 days | **Priority**: 🟡 Medium

- Bulk moderation actions
- Custom reporting
- Audit logging
- Tools: django-audit-log

---

## Development Workflow

### Daily Development Cycle
1. Pick a task from the current phase
2. Create a feature branch: `git checkout -b feature/task-name`
3. Write tests first (TDD approach)
4. Implement feature
5. Run tests: `pytest`
6. Run linting: `black . && flake8`
7. Commit with clear message: `git commit -m "feature: description"`
8. Create pull request for code review
9. Merge to main after approval

### Testing Command Reference
```bash
# Run all tests
pytest

# Run tests for specific app
pytest users/

# Run specific test file
pytest tests/test_models.py

# Run with coverage
pytest --cov=.

# Run specific test
pytest tests/test_models.py::TestItemModel::test_item_creation
```

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/feature-name

# Make changes and commit
git add .
git commit -m "feature: clear description"

# Push to remote
git push origin feature/feature-name

# After merge, clean up
git checkout main
git pull
git branch -d feature/feature-name
```

---

## Success Metrics

### Phase Completion
✅ All tasks marked complete  
✅ Tests passing (>80% coverage)  
✅ Code review approved  
✅ Deployed to staging  

### Code Quality
✅ No linting errors  
✅ No security vulnerabilities  
✅ Database queries optimized  
✅ API response time < 200ms  

### User Experience
✅ Mobile responsive  
✅ Accessibility standards met  
✅ Load time < 3 seconds  
✅ Intuitive navigation  

---

**Last Updated**: November 2025  
**Version**: 1.0  
**Estimated Total Duration**: 4-6 weeks (full MVP with optional phases 10-15)
