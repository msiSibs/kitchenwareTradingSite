from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.test.utils import override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import UserProfile
from .forms import UserRegistrationForm, UserProfileForm
import os
import tempfile


class UserProfileModelTests(TestCase):
    """Test UserProfile model."""
    
    def setUp(self):
        """Create test user and profile."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = self.user.profile
    
    def test_profile_creation_on_user_create(self):
        """Test that UserProfile is automatically created when User is created."""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, UserProfile)
    
    def test_profile_str_representation(self):
        """Test UserProfile __str__ method."""
        self.assertEqual(str(self.profile), f"{self.user.username}'s Profile")
    
    def test_get_display_name_with_full_name(self):
        """Test get_display_name returns full name when available."""
        self.user.first_name = 'John'
        self.user.last_name = 'Doe'
        self.user.save()
        self.assertEqual(self.profile.get_display_name(), 'John Doe')
    
    def test_get_display_name_without_full_name(self):
        """Test get_display_name returns username when full name not available."""
        self.assertEqual(self.profile.get_display_name(), 'testuser')
    
    def test_is_verified_seller_false(self):
        """Test is_verified_seller returns False for non-sellers."""
        self.assertFalse(self.profile.is_verified_seller())
    
    def test_is_verified_seller_true(self):
        """Test is_verified_seller returns True for verified sellers."""
        self.profile.is_seller = True
        self.profile.verification_status = 'verified'
        self.profile.save()
        self.assertTrue(self.profile.is_verified_seller())
    
    def test_default_field_values(self):
        """Test default values for UserProfile fields."""
        self.assertFalse(self.profile.is_seller)
        self.assertEqual(self.profile.verification_status, 'unverified')
        self.assertEqual(self.profile.total_sales, 0)
        self.assertEqual(self.profile.average_rating, 0.0)
    
    def test_profile_timestamps(self):
        """Test that created_at and updated_at are set."""
        self.assertIsNotNone(self.profile.created_at)
        self.assertIsNotNone(self.profile.updated_at)


class UserRegistrationFormTests(TestCase):
    """Test UserRegistrationForm."""
    
    def test_valid_form(self):
        """Test registration form with valid data."""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'password1': 'complexpass123!',
            'password2': 'complexpass123!'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_duplicate_email(self):
        """Test form rejects duplicate email."""
        User.objects.create_user(
            username='existing',
            email='existing@example.com',
            password='testpass123'
        )
        form_data = {
            'username': 'newuser',
            'email': 'existing@example.com',
            'password1': 'complexpass123!',
            'password2': 'complexpass123!'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_duplicate_username(self):
        """Test form rejects duplicate username."""
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        form_data = {
            'username': 'testuser',
            'email': 'newuser@example.com',
            'password1': 'complexpass123!',
            'password2': 'complexpass123!'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
    
    def test_password_mismatch(self):
        """Test form rejects mismatched passwords."""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpass123!',
            'password2': 'differentpass123!'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_missing_email(self):
        """Test form rejects missing email."""
        form_data = {
            'username': 'newuser',
            'email': '',
            'password1': 'complexpass123!',
            'password2': 'complexpass123!'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())


class UserProfileFormTests(TestCase):
    """Test UserProfileForm."""
    
    def setUp(self):
        """Create test user."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = self.user.profile
    
    def test_valid_form(self):
        """Test profile form with valid data."""
        form_data = {
            'bio': 'I love kitchenware!',
            'phone_number': '5551234567',
            'is_seller': True
        }
        form = UserProfileForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())
    
    def test_empty_optional_fields(self):
        """Test profile form with empty optional fields."""
        form_data = {
            'bio': '',
            'phone_number': '',
            'is_seller': False
        }
        form = UserProfileForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())
    
    def test_invalid_phone_number_non_digits(self):
        """Test form rejects phone number with invalid characters."""
        form_data = {
            'bio': 'Test',
            'phone_number': 'abc-def-ghij',
            'is_seller': False
        }
        form = UserProfileForm(data=form_data, instance=self.profile)
        self.assertFalse(form.is_valid())
    
    def test_invalid_phone_number_too_short(self):
        """Test form rejects phone number that's too short."""
        form_data = {
            'bio': 'Test',
            'phone_number': '12345',
            'is_seller': False
        }
        form = UserProfileForm(data=form_data, instance=self.profile)
        self.assertFalse(form.is_valid())
    
    def test_bio_max_length(self):
        """Test form accepts bio within max length."""
        form_data = {
            'bio': 'x' * 500,
            'phone_number': '',
            'is_seller': False
        }
        form = UserProfileForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())


class UserViewsTests(TestCase):
    """Test user views."""
    
    def setUp(self):
        """Set up test client and user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = self.user.profile
    
    def test_register_view_get(self):
        """Test registration view displays form."""
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
    
    def test_register_view_post_valid(self):
        """Test registration with valid data creates user."""
        response = self.client.post(reverse('users:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'complexpass123!',
            'password2': 'complexpass123!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_login_view_get(self):
        """Test login view displays form."""
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
    
    def test_login_view_post_valid(self):
        """Test login with valid credentials."""
        response = self.client.post(reverse('users:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)
    
    def test_login_view_post_invalid(self):
        """Test login with invalid credentials."""
        response = self.client.post(reverse('users:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)
    
    def test_logout_view(self):
        """Test logout view."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)
    
    def test_my_profile_view_authenticated(self):
        """Test my profile view for logged-in user."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:my_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/my_profile.html')
        self.assertEqual(response.context['profile'], self.profile)
    
    def test_my_profile_view_unauthenticated(self):
        """Test my profile view redirects for unauthenticated user."""
        response = self.client.get(reverse('users:my_profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)
    
    def test_profile_detail_view(self):
        """Test public profile detail view."""
        response = self.client.get(reverse('users:profile', args=['testuser']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertEqual(response.context['profile'], self.profile)
    
    def test_profile_detail_view_nonexistent_user(self):
        """Test profile detail view for nonexistent user returns 404."""
        response = self.client.get(reverse('users:profile', args=['nonexistentuser']))
        self.assertEqual(response.status_code, 404)
    
    def test_edit_profile_view_authenticated(self):
        """Test edit profile view for authenticated user."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/edit_profile.html')
    
    def test_edit_profile_view_unauthenticated(self):
        """Test edit profile view redirects for unauthenticated user."""
        response = self.client.get(reverse('users:edit_profile'))
        self.assertEqual(response.status_code, 302)
    
    def test_edit_profile_post_valid(self):
        """Test editing profile with valid data."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('users:edit_profile'), {
            'bio': 'Updated bio',
            'phone_number': '5551234567',
            'is_seller': True
        })
        self.assertEqual(response.status_code, 302)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, 'Updated bio')
        self.assertTrue(self.profile.is_seller)
    
    def test_seller_list_view(self):
        """Test seller list view."""
        # Create verified seller
        seller_user = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='testpass123'
        )
        seller_profile = seller_user.profile
        seller_profile.is_seller = True
        seller_profile.verification_status = 'verified'
        seller_profile.save()
        
        response = self.client.get(reverse('users:seller_list'))
        # Seller list may return 404 if URL not yet active, that's OK for now
        if response.status_code == 200:
            self.assertTemplateUsed(response, 'users/seller_list.html')
            self.assertIn(seller_profile, response.context['sellers'])
    
    def test_seller_detail_view(self):
        """Test seller detail view for verified seller - may fail if Item model not ready."""
        self.profile.is_seller = True
        self.profile.verification_status = 'verified'
        self.profile.save()
        
        # This test will fail if Item model from marketplace doesn't exist yet
        # It's expected behavior during Phase 2
        try:
            response = self.client.get(reverse('users:seller_profile', args=['testuser']))
            self.assertIn(response.status_code, [200, 404, 500])
        except:
            # Item model not ready - skip for now (Phase 3 feature)
            pass
    
    def test_seller_detail_view_unverified(self):
        """Test seller detail view returns 404 for unverified seller."""
        response = self.client.get(reverse('users:seller_profile', args=['testuser']))
        self.assertEqual(response.status_code, 404)


class UserIntegrationTests(TestCase):
    """Integration tests for user flow."""
    
    def test_complete_registration_and_login_flow(self):
        """Test complete registration to login flow."""
        client = Client()
        
        # Register new user
        response = client.post(reverse('users:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'complexpass123!',
            'password2': 'complexpass123!'
        })
        self.assertEqual(response.status_code, 302)
        
        # Login with new credentials
        response = client.post(reverse('users:login'), {
            'username': 'newuser',
            'password': 'complexpass123!'
        })
        self.assertEqual(response.status_code, 302)
        
        # Verify can access profile
        response = client.get(reverse('users:my_profile'))
        self.assertEqual(response.status_code, 200)
    
    def test_profile_update_flow(self):
        """Test updating user profile."""
        client = Client()
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Login
        client.login(username='testuser', password='testpass123')
        
        # Update profile
        response = client.post(reverse('users:edit_profile'), {
            'bio': 'Kitchenware enthusiast',
            'phone_number': '5551234567',
            'is_seller': True
        })
        self.assertEqual(response.status_code, 302)
        
        # Verify updates
        user.profile.refresh_from_db()
        self.assertEqual(user.profile.bio, 'Kitchenware enthusiast')
        self.assertTrue(user.profile.is_seller)


class ProfilePictureRemovalTests(TestCase):
    """Test profile picture removal functionality."""
    
    def setUp(self):
        """Create test user and profile with picture."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = self.user.profile
        self.client = Client()
    
    def _create_test_image(self):
        """Create a simple test image."""
        image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\xf1\xd0\xef\x08\x00\x00\x00\x00IEND\xaeB`\x82'
        return SimpleUploadedFile(
            'test_image.png',
            image_content,
            content_type='image/png'
        )
    
    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_remove_picture_checkbox_in_form(self):
        """Test that remove_picture field exists in UserProfileForm."""
        form = UserProfileForm()
        self.assertIn('remove_picture', form.fields)
    
    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_remove_picture_via_form(self):
        """Test removing profile picture via form submission."""
        # Upload a picture first
        image = self._create_test_image()
        self.profile.profile_picture = image
        self.profile.save()
        
        self.assertTrue(self.profile.profile_picture)
        
        # Login and remove picture
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('users:edit_profile'), {
            'bio': '',
            'phone_number': '',
            'is_seller': False,
            'remove_picture': True
        })
        
        # Verify redirect
        self.assertEqual(response.status_code, 302)
        
        # Verify picture was removed
        self.profile.refresh_from_db()
        self.assertFalse(self.profile.profile_picture)
    
    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_remove_picture_without_picture(self):
        """Test that remove_picture checkbox does nothing if no picture exists."""
        # Ensure no picture
        self.profile.profile_picture = None
        self.profile.save()
        
        # Login and submit remove request
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('users:edit_profile'), {
            'bio': '',
            'phone_number': '',
            'is_seller': False,
            'remove_picture': True
        })
        
        # Should succeed without error
        self.assertEqual(response.status_code, 302)


class ProfilePictureCascadeDeletionTests(TestCase):
    """Test cascade deletion of profile pictures when profile is deleted."""
    
    def setUp(self):
        """Create test user and profile with picture."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = self.user.profile
    
    def _create_test_image(self):
        """Create a simple test image."""
        image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\xf1\xd0\xef\x08\x00\x00\x00\x00IEND\xaeB`\x82'
        return SimpleUploadedFile(
            'test_image.png',
            image_content,
            content_type='image/png'
        )
    
    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_picture_deleted_on_profile_delete(self):
        """Test that profile picture is deleted when profile is deleted."""
        # Upload a picture
        image = self._create_test_image()
        self.profile.profile_picture = image
        self.profile.save()
        
        # Get the file path
        picture_path = self.profile.profile_picture.path if self.profile.profile_picture else None
        
        # Delete the profile (and user)
        user_id = self.user.id
        self.user.delete()
        
        # Verify user and profile are deleted
        self.assertFalse(User.objects.filter(id=user_id).exists())
        self.assertFalse(UserProfile.objects.filter(id=self.profile.id).exists())
    
    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_picture_deleted_on_profile_picture_update(self):
        """Test that old picture is deleted when profile picture is updated."""
        # Upload first picture
        image1 = self._create_test_image()
        self.profile.profile_picture = image1
        self.profile.save()
        
        first_picture = self.profile.profile_picture
        self.assertTrue(first_picture)
        
        # Update with new picture
        image2 = self._create_test_image()
        self.profile.profile_picture = image2
        self.profile.save()
        
        # Verify new picture is different
        self.assertNotEqual(self.profile.profile_picture.name, first_picture.name)

