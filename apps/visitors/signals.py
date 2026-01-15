"""
Visitors signals - Trigger notifications on new inquiries
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import VisitorInquiry


@receiver(post_save, sender=VisitorInquiry)
def notify_on_new_inquiry(sender, instance, created, **kwargs):
    """
    Send notifications when a new inquiry is created.
    """
    if created:
        # Import here to avoid circular imports
        from apps.notifications.services import email_service, whatsapp_service

        # Send email notification directly (no Celery needed for local dev)
        try:
            email_service.send_inquiry_notification(instance)
        except Exception as e:
            print(f"Email error: {e}")

        # Send WhatsApp notification if configured
        try:
            if whatsapp_service.is_configured():
                message = whatsapp_service.format_inquiry_message(instance)
                whatsapp_service.send_message(
                    settings.COMMUNITY_WHATSAPP,
                    message,
                    instance
                )
        except Exception as e:
            print(f"WhatsApp error: {e}")
