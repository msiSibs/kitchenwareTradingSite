from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class UserProfile(models.Model):
    """Extended user profile with seller capabilities and ratings."""
    
    VERIFICATION_CHOICES = [
        ('unverified', 'Unverified'),
        ('verified', 'Verified'),
        ('suspended', 'Suspended'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, max_length=500, help_text="Short biography (max 500 characters)")
    profile_picture = models.ImageField(
        upload_to='profiles/%Y/%m/%d/', 
        null=True, 
        blank=True,
        help_text="Profile picture (recommended: square image, 1MB max)"
    )
    phone_number = models.CharField(max_length=15, blank=True, help_text="Contact phone number")
    
    # Seller information
    is_seller = models.BooleanField(default=False, help_text="Is this user a seller?")
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_CHOICES,
        default='unverified',
        help_text="Seller account verification status"
    )
    
    # Seller statistics
    total_sales = models.IntegerField(default=0, help_text="Total number of items sold")
    average_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.0,
        help_text="Average rating from buyers (0.0 to 5.0)"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        indexes = [
            models.Index(fields=['is_seller', '-average_rating']),
            models.Index(fields=['verification_status']),
        ]
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_display_name(self):
        """Return user's display name (full name or username)."""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username
    
    def is_verified_seller(self):
        """Check if user is a verified seller."""
        return self.is_seller and self.verification_status == 'verified'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a UserProfile when a new User is created."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Automatically save the UserProfile when the User is saved."""
    instance.profile.save()


@receiver(pre_delete, sender=UserProfile)
def delete_user_profile_picture(sender, instance, **kwargs):
    """Delete the profile picture file when UserProfile is deleted."""
    if instance.profile_picture:
        # Delete the image file from storage
        instance.profile_picture.delete(save=False)
