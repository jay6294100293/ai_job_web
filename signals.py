# Register signals
from django.db.models.signals import post_save
from django.dispatch import receiver

from auth_app.models import CustomUser
from core.models import UserAPIUsage, KeywordExtraction


@receiver(post_save, sender=CustomUser)
def create_user_api_usage(sender, instance, created, **kwargs):
    """Create UserAPIUsage instance when a new user is created."""
    if created:
        UserAPIUsage.objects.create(user=instance)

@receiver(post_save, sender=KeywordExtraction)
def update_user_api_usage(sender, instance, created, **kwargs):
    """Update UserAPIUsage when a new keyword extraction is performed."""
    if created and instance.success:
        api_usage, _ = UserAPIUsage.objects.get_or_create(user=instance.user)
        api_usage.update_usage(instance.cost, instance.provider)