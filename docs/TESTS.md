# 🧪 Test Suites

## Overview
Comprehensive test suites for Users and Marketplace applications.

**Overall Status**: ✅ **ALL 72 TESTS PASSING (43 Users + 29 Marketplace)**

---

## Users App Test Suite

**Status**: ✅ **ALL 36 TESTS PASSING**

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
- All authentication flows properly tested
- Form validation comprehensive
- Model signals tested for auto-profile creation and image cleanup
- Permission checks validated (LoginRequiredMixin, UserPassesTestMixin)
- Profile picture removal and cascade deletion fully tested with temporary media directories

---

## Marketplace App Test Suite

**Status**: ✅ **ALL 29 TESTS PASSING (November 20, 2025)**

### 1. Category Model Tests (4 tests)
- ✅ `test_category_creation` - Category can be created with name and icon
- ✅ `test_category_str` - Category string representation displays name
- ✅ `test_category_unique_name` - Enforces unique category names
- ✅ `test_category_ordering` - Categories ordered alphabetically by name

### 2. Item Model Tests (8 tests)
- ✅ `test_item_creation` - Item can be created with all fields
- ✅ `test_item_str` - Item string representation displays title
- ✅ `test_item_seller_relationship` - Item properly associates with seller
- ✅ `test_item_condition_choices` - Validates condition field choices
- ✅ `test_item_get_condition_display` - Condition displays human-readable format
- ✅ `test_item_inactive` - Soft delete sets is_active=False without removing from DB
- ✅ `test_item_ordering` - Items ordered by creation date descending
- ✅ `test_item_ordering` - Most recent items appear first

### 3. Item Image Model Tests (3 tests)
- ✅ `test_item_image_creation` - ItemImage can be created and attached to item
- ✅ `test_item_multiple_images` - Items can have multiple images
- ✅ `test_item_image_primary` - Primary image can be selected and tracked

### 4. Item List View Tests (4 tests)
- ✅ `test_item_list_view_accessible` - Marketplace list view displays at /marketplace/
- ✅ `test_item_list_view_template` - Uses correct template (listing_list.html)
- ✅ `test_item_list_category_filter` - Category filtering works via query parameter
- ✅ `test_item_list_shows_active_items` - Only active items displayed, inactive items hidden

### 5. Item Detail View Tests (2 tests)
- ✅ `test_item_detail_view_accessible` - Item detail view displays item page
- ✅ `test_item_detail_shows_item_info` - Item details (title, description, price) shown correctly

### 6. Item Create View Tests (4 tests)
- ✅ `test_create_item_requires_login` - Unauthenticated users redirected to login
- ✅ `test_create_item_requires_seller_status` - Non-sellers redirected to profile edit
- ✅ `test_seller_can_access_create_view` - Sellers can access item creation form
- ✅ `test_seller_can_create_item` - Sellers can successfully create new items

### 7. Item Update View Tests (2 tests)
- ✅ `test_seller_can_update_own_item` - Sellers can update their own items
- ✅ `test_other_seller_cannot_update_item` - Other sellers cannot update items they don't own

### 8. Item Delete View Tests (2 tests)
- ✅ `test_seller_can_delete_own_item` - Sellers can soft-delete own items
- ✅ `test_other_seller_cannot_delete_item` - Other sellers cannot delete items they don't own

### 9. Integration Test (1 test)
- ✅ `test_complete_marketplace_flow` - Full workflow: view marketplace → login → create → update → soft delete

## Running Tests

### Run all marketplace tests:
```bash
python3 manage.py test marketplace
```

### Run all users tests:
```bash
python3 manage.py test users
```

### Run all tests:
```bash
python3 manage.py test
```

### Run with verbose output:
```bash
python3 manage.py test marketplace --verbosity=2
```

### Run specific test class:
```bash
python3 manage.py test marketplace.tests.ItemModelTests
```

### Run specific test:
```bash
python3 manage.py test marketplace.tests.ItemModelTests.test_item_creation
```

## Test Statistics
- **Users Tests**: 36 passed ✅
- **Marketplace Tests**: 29 passed ✅
- **Total Tests**: 65 passed ✅
- **Failed**: 0
- **Errors**: 0
- **Coverage**: Models, Forms, Views, Integration, Permissions, Image Handling, Soft Delete

## Key Features Tested
✅ Model creation and validation  
✅ Relationship integrity (sellers, categories, images)  
✅ Permission enforcement (seller authorization)  
✅ CRUD operations (create, read, update, soft-delete)  
✅ Filtering and querying  
✅ View accessibility and response codes  
✅ Template usage and content  
✅ Complete user workflows  
✅ Soft delete functionality  
✅ Image handling and attachments  

## Future Test Enhancements
- Add tests for messaging system (Phase 4)
- Add tests for transaction management (Phase 4)
- Add tests for review system (Phase 4)
- Add tests for search and filtering (Phase 4)
- Add performance tests for large datasets
- Add edge case tests for form validation
- Add admin panel tests
