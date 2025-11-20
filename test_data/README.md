# Test Data Directory

This directory contains test images and sample data for testing marketplace functionality.

## Contents

- **images/** - Sample product images for testing uploads
- **sample_items.json** - Sample item data for bulk creation (Phase 4+)
- **test_users.json** - Sample user/seller data

## Usage

### For Manual Testing
1. Upload images from the `images/` folder when creating listings
2. Use the images to test image validation, upload, and deletion functionality

### For Bulk Data Loading (Future)
```bash
python3 manage.py loaddata test_data/test_users.json
python3 manage.py loaddata test_data/sample_items.json
```

## Image Specifications

All test images are:
- Format: PNG, JPG, WebP
- Size: Varies (500x500px to 2000x2000px)
- Purpose: Testing image upload, storage, and display functionality

## Notes

- This directory is excluded from Git (see .gitignore)
- Safe to delete; can be recreated or regenerated anytime
- Use for development and testing only
