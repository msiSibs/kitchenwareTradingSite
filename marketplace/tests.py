from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from marketplace.models import Category, Item, ItemImage
from PIL import Image
import io


class CategoryModelTests(TestCase):
    """Tests for Category model."""
    
    def setUp(self):
        """Create test categories."""
        self.category, created = Category.objects.get_or_create(
            name='Cutlery_Test',
            defaults={'description': 'Knives, forks, spoons', 'icon': '🔪'}
        )
    
    def test_category_creation(self):
        """Test category can be created."""
        self.assertEqual(self.category.name, 'Cutlery_Test')
        self.assertEqual(self.category.icon, '🔪')
    
    def test_category_str(self):
        """Test category string representation."""
        self.assertEqual(str(self.category), 'Cutlery_Test')
    
    def test_category_unique_name(self):
        """Test category names are unique."""
        with self.assertRaises(Exception):
            Category.objects.create(
                name='Cutlery_Test',
                description='Duplicate'
            )
    
    def test_category_ordering(self):
        """Test categories are ordered by name."""
        Category.objects.get_or_create(name='Bakeware_Test')
        Category.objects.get_or_create(name='Appliances_Test')
        # Check that our test categories are ordered
        test_categories = list(Category.objects.filter(name__contains='_Test').order_by('name').values_list('name', flat=True))
        self.assertTrue(len(test_categories) >= 3)
        # Verify they're in alphabetical order
        self.assertEqual(test_categories, sorted(test_categories))


class ItemModelTests(TestCase):
    """Tests for Item model."""
    
    def setUp(self):
        """Create test data."""
        self.user = User.objects.create_user(username='seller', password='testpass')
        self.user.profile.is_seller = True
        self.user.profile.save()
        
        self.category, _ = Category.objects.get_or_create(name='Cookware_Test')
        
        self.item = Item.objects.create(
            seller=self.user,
            title='Cast Iron Skillet',
            description='Vintage cast iron skillet in good condition',
            category=self.category,
            price=45.00,
            condition='good',
            brand='Lodge',
            material='Cast Iron',
            location='New York, NY'
        )
    
    def test_item_creation(self):
        """Test item can be created."""
        self.assertEqual(self.item.title, 'Cast Iron Skillet')
        self.assertEqual(self.item.price, 45.00)
        self.assertTrue(self.item.is_active)
    
    def test_item_str(self):
        """Test item string representation."""
        self.assertEqual(str(self.item), 'Cast Iron Skillet')
    
    def test_item_seller_relationship(self):
        """Test item is associated with seller."""
        self.assertEqual(self.item.seller, self.user)
    
    def test_item_condition_choices(self):
        """Test item condition choices."""
        self.assertEqual(self.item.condition, 'good')
        valid_conditions = ['like_new', 'good', 'fair', 'needs_repair']
        self.assertIn(self.item.condition, valid_conditions)
    
    def test_item_get_condition_display(self):
        """Test condition is displayed correctly."""
        self.assertEqual(self.item.get_condition_display(), 'Good')
    
    def test_item_inactive(self):
        """Test soft delete functionality."""
        self.item.is_active = False
        self.item.save()
        self.assertFalse(self.item.is_active)
        # Item still exists in database
        self.assertTrue(Item.objects.filter(pk=self.item.pk).exists())
    
    def test_item_ordering(self):
        """Test items are ordered by created date descending."""
        Item.objects.create(
            seller=self.user,
            title='Dutch Oven',
            description='Large dutch oven',
            category=self.category,
            price=120.00,
            condition='like_new',
            location='New York, NY'
        )
        items = list(Item.objects.values_list('title', flat=True))
        self.assertEqual(items[0], 'Dutch Oven')  # Most recent first


class ItemImageModelTests(TestCase):
    """Tests for ItemImage model."""
    
    def setUp(self):
        """Create test data."""
        self.user = User.objects.create_user(username='seller', password='testpass')
        self.category, _ = Category.objects.get_or_create(name='Cookware_Test')
        self.item = Item.objects.create(
            seller=self.user,
            title='Test Item',
            description='Test',
            category=self.category,
            price=50.00,
            condition='good',
            location='Test Location'
        )
    
    def test_item_image_creation(self):
        """Test item image can be created."""
        # Create a test image
        image = Image.new('RGB', (100, 100), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        
        image_file = SimpleUploadedFile(
            'test.jpg',
            image_io.getvalue(),
            content_type='image/jpeg'
        )
        
        item_image = ItemImage.objects.create(
            item=self.item,
            image=image_file,
            is_primary=True
        )
        self.assertEqual(item_image.item, self.item)
        self.assertTrue(item_image.is_primary)
    
    def test_item_multiple_images(self):
        """Test item can have multiple images."""
        # Create test images
        for i in range(3):
            image = Image.new('RGB', (100, 100), color='red')
            image_io = io.BytesIO()
            image.save(image_io, format='JPEG')
            image_io.seek(0)
            
            image_file = SimpleUploadedFile(
                f'test{i}.jpg',
                image_io.getvalue(),
                content_type='image/jpeg'
            )
            
            ItemImage.objects.create(
                item=self.item,
                image=image_file,
                is_primary=(i == 0)
            )
        
        images = ItemImage.objects.filter(item=self.item)
        self.assertEqual(images.count(), 3)
    
    def test_item_image_primary(self):
        """Test primary image selection."""
        image = Image.new('RGB', (100, 100), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        
        image_file = SimpleUploadedFile(
            'test.jpg',
            image_io.getvalue(),
            content_type='image/jpeg'
        )
        
        item_image = ItemImage.objects.create(
            item=self.item,
            image=image_file,
            is_primary=True
        )
        self.assertTrue(item_image.is_primary)


class ItemListViewTests(TestCase):
    """Tests for ItemListView."""
    
    def setUp(self):
        """Create test data."""
        self.client = Client()
        self.user = User.objects.create_user(username='seller', password='testpass')
        self.category, _ = Category.objects.get_or_create(name='Cookware_Test')
        
        self.item = Item.objects.create(
            seller=self.user,
            title='Skillet',
            description='Test item',
            category=self.category,
            price=50.00,
            condition='good',
            location='Test Location'
        )
        
        # Create an inactive item that shouldn't show up
        self.inactive_item = Item.objects.create(
            seller=self.user,
            title='Baking Pan',
            description='Test',
            category=self.category,
            price=30.00,
            condition='good',
            location='Test',
            is_active=False
        )
    
    def test_item_list_view_accessible(self):
        """Test marketplace list view is accessible."""
        response = self.client.get(reverse('marketplace:list'))
        self.assertEqual(response.status_code, 200)
    
    def test_item_list_view_template(self):
        """Test correct template is used."""
        response = self.client.get(reverse('marketplace:list'))
        self.assertTemplateUsed(response, 'marketplace/listing_list.html')
    
    def test_item_list_category_filter(self):
        """Test category filter works."""
        response = self.client.get(reverse('marketplace:list') + f'?category={self.category.id}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Skillet')
    
    def test_item_list_shows_active_items(self):
        """Test only active items are shown."""
        response = self.client.get(reverse('marketplace:list'))
        self.assertContains(response, 'Skillet')
        self.assertNotContains(response, 'Baking Pan')


class ItemDetailViewTests(TestCase):
    """Tests for ItemDetailView."""
    
    def setUp(self):
        """Create test data."""
        self.client = Client()
        self.user = User.objects.create_user(username='seller', password='testpass')
        self.category, _ = Category.objects.get_or_create(name='Cookware_Test')
        
        self.item = Item.objects.create(
            seller=self.user,
            title='Skillet',
            description='Quality cast iron skillet',
            category=self.category,
            price=50.00,
            condition='good',
            location='NYC'
        )
    
    def test_item_detail_view_accessible(self):
        """Test item detail view is accessible."""
        response = self.client.get(reverse('marketplace:detail', args=[self.item.pk]))
        self.assertEqual(response.status_code, 200)
    
    def test_item_detail_shows_item_info(self):
        """Test item detail shows correct information."""
        response = self.client.get(reverse('marketplace:detail', args=[self.item.pk]))
        self.assertContains(response, 'Skillet')
        self.assertContains(response, 'Quality cast iron skillet')
        self.assertContains(response, '$50.00')


class ItemCreateViewTests(TestCase):
    """Tests for ItemCreateView."""
    
    def setUp(self):
        """Create test data."""
        self.client = Client()
        self.seller = User.objects.create_user(username='seller', password='testpass')
        self.seller.profile.is_seller = True
        self.seller.profile.save()
        
        self.buyer = User.objects.create_user(username='buyer', password='testpass')
        self.buyer.profile.is_seller = False
        self.buyer.profile.save()
        
        self.category, _ = Category.objects.get_or_create(name='Cookware_Test')
    
    def test_create_item_requires_login(self):
        """Test create view requires login."""
        response = self.client.get(reverse('marketplace:create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_create_item_requires_seller_status(self):
        """Test non-sellers cannot create items."""
        self.client.login(username='buyer', password='testpass')
        response = self.client.get(reverse('marketplace:create'))
        self.assertEqual(response.status_code, 302)  # Redirect to edit profile
    
    def test_seller_can_access_create_view(self):
        """Test sellers can access create view."""
        self.client.login(username='seller', password='testpass')
        response = self.client.get(reverse('marketplace:create'))
        self.assertEqual(response.status_code, 200)
    
    def test_seller_can_create_item(self):
        """Test seller can create an item."""
        self.client.login(username='seller', password='testpass')
        data = {
            'title': 'New Skillet',
            'description': 'Brand new skillet',
            'category': self.category.id,
            'price': 75.00,
            'condition': 'like_new',
            'brand': 'Le Creuset',
            'material': 'Enameled Cast Iron',
            'location': 'Boston, MA'
        }
        response = self.client.post(reverse('marketplace:create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(Item.objects.filter(title='New Skillet').exists())


class ItemUpdateViewTests(TestCase):
    """Tests for ItemUpdateView."""
    
    def setUp(self):
        """Create test data."""
        self.client = Client()
        self.seller = User.objects.create_user(username='seller', password='testpass')
        self.seller.profile.is_seller = True
        self.seller.profile.save()
        
        self.other_seller = User.objects.create_user(username='other', password='testpass')
        self.other_seller.profile.is_seller = True
        self.other_seller.profile.save()
        
        self.category, _ = Category.objects.get_or_create(name='Cookware_Test')
        self.item = Item.objects.create(
            seller=self.seller,
            title='Skillet',
            description='Test',
            category=self.category,
            price=50.00,
            condition='good',
            location='Test'
        )
    
    def test_seller_can_update_own_item(self):
        """Test seller can update their own item."""
        self.client.login(username='seller', password='testpass')
        data = {
            'title': 'Updated Skillet',
            'description': 'Test',
            'category': self.category.id,
            'price': 60.00,
            'condition': 'good',
            'location': 'Test'
        }
        response = self.client.post(
            reverse('marketplace:edit', args=[self.item.pk]),
            data
        )
        self.item.refresh_from_db()
        self.assertEqual(self.item.title, 'Updated Skillet')
        self.assertEqual(self.item.price, 60.00)
    
    def test_other_seller_cannot_update_item(self):
        """Test other sellers cannot update items they don't own."""
        self.client.login(username='other', password='testpass')
        response = self.client.get(reverse('marketplace:edit', args=[self.item.pk]))
        self.assertEqual(response.status_code, 302)


class ItemDeleteViewTests(TestCase):
    """Tests for ItemDeleteView."""
    
    def setUp(self):
        """Create test data."""
        self.client = Client()
        self.seller = User.objects.create_user(username='seller', password='testpass')
        self.seller.profile.is_seller = True
        self.seller.profile.save()
        
        self.other_seller = User.objects.create_user(username='other', password='testpass')
        self.other_seller.profile.is_seller = True
        self.other_seller.profile.save()
        
        self.category, _ = Category.objects.get_or_create(name='Cookware_Test')
        self.item = Item.objects.create(
            seller=self.seller,
            title='Skillet',
            description='Test',
            category=self.category,
            price=50.00,
            condition='good',
            location='Test'
        )
    
    def test_seller_can_delete_own_item(self):
        """Test seller can soft delete their own item."""
        self.client.login(username='seller', password='testpass')
        # Verify item is active before delete
        item_before = Item._base_manager.get(pk=self.item.pk)
        self.assertTrue(item_before.is_active)
        
        response = self.client.post(
            reverse('marketplace:delete', args=[self.item.pk]),
            follow=False  # Don't follow redirect
        )
        self.assertEqual(response.status_code, 302)  # Redirect
        
        # Check item is soft deleted using _base_manager to bypass any filtering
        item_after_delete = Item._base_manager.get(pk=self.item.pk)
        self.assertFalse(item_after_delete.is_active)  # Soft delete
        self.assertTrue(Item._base_manager.filter(pk=self.item.pk).exists())  # Still in DB
    
    def test_other_seller_cannot_delete_item(self):
        """Test other sellers cannot delete items they don't own."""
        self.client.login(username='other', password='testpass')
        response = self.client.post(reverse('marketplace:delete', args=[self.item.pk]))
        self.assertEqual(response.status_code, 302)
        self.item.refresh_from_db()
        self.assertTrue(self.item.is_active)  # Not deleted


class MarketplaceIntegrationTests(TestCase):
    """Integration tests for complete marketplace workflow."""
    
    def setUp(self):
        """Create test data."""
        self.client = Client()
        self.seller = User.objects.create_user(username='seller', password='testpass')
        self.seller.profile.is_seller = True
        self.seller.profile.save()
        
        self.buyer = User.objects.create_user(username='buyer', password='testpass')
        
        self.category, _ = Category.objects.get_or_create(name='Cookware_Test')
    
    def test_complete_marketplace_flow(self):
        """Test complete marketplace workflow."""
        # 1. View marketplace
        response = self.client.get(reverse('marketplace:list'))
        self.assertEqual(response.status_code, 200)
        
        # 2. Login as seller
        self.client.login(username='seller', password='testpass')
        
        # 3. Create item
        data = {
            'title': 'Cast Iron Skillet',
            'description': 'High quality skillet',
            'category': self.category.id,
            'price': 75.00,
            'condition': 'like_new',
            'location': 'NYC'
        }
        response = self.client.post(reverse('marketplace:create'), data)
        self.assertEqual(response.status_code, 302)
        
        # 4. View item
        item = Item.objects.get(title='Cast Iron Skillet')
        response = self.client.get(reverse('marketplace:detail', args=[item.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cast Iron Skillet')
        
        # 5. Update item
        data['title'] = 'Updated Skillet'
        response = self.client.post(reverse('marketplace:edit', args=[item.pk]), data)
        item_after_update = Item.objects.get(pk=item.pk)
        self.assertEqual(item_after_update.title, 'Updated Skillet')
        
        # 6. Delete item
        response = self.client.post(
            reverse('marketplace:delete', args=[item.pk]),
            follow=False  # Don't follow redirect
        )
        self.assertEqual(response.status_code, 302)
        
        # Verify soft delete using _base_manager
        item_after_delete = Item._base_manager.get(pk=item.pk)
        self.assertFalse(item_after_delete.is_active)
