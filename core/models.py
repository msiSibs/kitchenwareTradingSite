"""
Core models - Minimal, no models needed for core app initially
"""

from django.db import models


class TimeStampedModel(models.Model):
    """Abstract model for models that need created/updated timestamps"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
