"""
Visitors signals - Trigger notifications on new inquiries
"""

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import VisitorInquiry


@receiver(post_save, sender=VisitorInquiry)
def notify_on_new_inquiry(sender, instance, created, **kwargs):
    """
    Send notifications when a new inquiry is created.
    """
    if created:
        # Import here to avoid circular imports
        from apps.notifications.tasks import (
            send_inquiry_email_notification,
            send_inquiry_whatsapp_notification,
        )

        # Queue email notification
        send_inquiry_email_notification.delay(instance.id)

        # Queue WhatsApp notification
        send_inquiry_whatsapp_notification.delay(instance.id)
