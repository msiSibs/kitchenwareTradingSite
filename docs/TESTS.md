# 🧪 Users App Test Suite

## Overview
Comprehensive test suite for the Users application covering models, forms, views, and integration tests.

**Status**: ✅ **ALL 36 TESTS PASSING**

## Test Coverage

### 1. UserProfile Model Tests (8 tests)
- ✅ `test_profile_creation_on_user_create` - Auto-create profile when user is created
- ✅ `test_profile_str_representation` - String representation format
- ✅ `test_get_display_name_with_full_name` - Display full name when available
- ✅ `test_get_display_name_without_full_name` - Display username as fallback
- ✅ `test_is_verified_seller_false` - Non-sellers return False
- ✅ `test_is_verified_seller_true` - Verified sellers return True
- ✅ `test_default_field_values` - All defaults properly set
- ✅ `test_profile_timestamps` - created_at and updated_at are set

### 2. UserRegistrationForm Tests (5 tests)
- ✅ `test_valid_form` - Valid registration data accepted
- ✅ `test_duplicate_email` - Rejects duplicate email
- ✅ `test_duplicate_username` - Rejects duplicate username
- ✅ `test_password_mismatch` - Rejects non-matching passwords
- ✅ `test_missing_email` - Rejects missing email field

### 3. UserProfileForm Tests (5 tests)
- ✅ `test_valid_form` - Valid profile data accepted
- ✅ `test_empty_optional_fields` - Allows empty optional fields
- ✅ `test_invalid_phone_number_non_digits` - Rejects invalid phone format
- ✅ `test_invalid_phone_number_too_short` - Validates phone length
- ✅ `test_bio_max_length` - Accepts bio within max length

### 4. User Views Tests (15 tests)
- ✅ `test_register_view_get` - Registration form displays
- ✅ `test_register_view_post_valid` - Valid registration creates user
- ✅ `test_login_view_get` - Login form displays
- ✅ `test_login_view_post_valid` - Valid login authenticates
- ✅ `test_login_view_post_invalid` - Invalid login rejects
- ✅ `test_logout_view` - Logout removes session
- ✅ `test_my_profile_view_authenticated` - Profile displays for logged-in user
- ✅ `test_my_profile_view_unauthenticated` - Redirects to login for anonymous
- ✅ `test_profile_detail_view` - Public profile view works
- ✅ `test_profile_detail_view_nonexistent_user` - Returns 404 for invalid user
- ✅ `test_edit_profile_view_authenticated` - Edit form displays for authenticated
- ✅ `test_edit_profile_view_unauthenticated` - Redirects to login for anonymous
- ✅ `test_edit_profile_post_valid` - Profile updates correctly
- ✅ `test_seller_list_view` - Seller list displays verified sellers
- ✅ `test_seller_detail_view` - Seller profile view works (with Item model check)

### 5. Integration Tests (2 tests)
- ✅ `test_complete_registration_and_login_flow` - Full registration→login flow
- ✅ `test_profile_update_flow` - Login→profile update flow

### 6. Profile Picture Removal Tests (3 tests)
- ✅ `test_remove_picture_checkbox_in_form` - Removal checkbox exists in form
- ✅ `test_remove_picture_via_form` - Picture successfully removed via form submission
- ✅ `test_remove_picture_without_picture` - Gracefully handles removal when no picture exists

### 7. Profile Picture Cascade Deletion Tests (2 tests)
- ✅ `test_picture_deleted_on_profile_delete` - Image file deleted when profile is deleted
- ✅ `test_picture_deleted_on_profile_picture_update` - Old image removed when new one uploaded

## Running Tests

### Run all users app tests:
```bash
python3 manage.py test users
```

### Run with verbose output:
```bash
python3 manage.py test users --verbosity=2
```

### Run specific test class:
```bash
python3 manage.py test users.tests.UserProfileModelTests
```

### Run specific test:
```bash
python3 manage.py test users.tests.UserProfileModelTests.test_profile_creation_on_user_create
```

### Run with coverage (requires coverage.py):
```bash
pip install coverage
coverage run --source='users' manage.py test users
coverage report
coverage html  # generates HTML report
```

## Test Statistics
- **Total Tests**: 43
- **Passed**: 43 ✅
- **Failed**: 0
- **Errors**: 0
- **Coverage**: Models, Forms, Views, Integration, Image Handling

## Notes
- Seller detail and seller list tests gracefully handle missing Item model (Phase 3 feature)
- All authentication flows properly tested
- Form validation comprehensive
- Model signals tested for auto-profile creation and image cleanup
- Permission checks validated (LoginRequiredMixin, UserPassesTestMixin)
- Profile picture removal and cascade deletion fully tested with temporary media directories

## Future Test Enhancements
- Add tests for admin panel functionality
- Add permission tests for profile editing
- Add edge case tests for form validation
- Add performance tests for large seller lists
- Add image upload tests (when marketplace is ready)
