"""
Celery tasks for sending notifications asynchronously.
"""

import logging

from celery import shared_task
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_inquiry_email_notification(self, inquiry_id: int):
    """
    Send email notification about new inquiry to the community.
    """
    from apps.visitors.models import VisitorInquiry
    from .services import email_service

    try:
        inquiry = VisitorInquiry.objects.get(id=inquiry_id)
        email_service.send_inquiry_notification(inquiry)
        logger.info(f"Email notification sent for inquiry {inquiry_id}")

    except VisitorInquiry.DoesNotExist:
        logger.error(f"Inquiry {inquiry_id} not found")

    except Exception as e:
        logger.error(f"Email notification failed: {str(e)}")
        self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_inquiry_whatsapp_notification(self, inquiry_id: int):
    """
    Send WhatsApp notification about new inquiry to the community.
    """
    from apps.visitors.models import VisitorInquiry
    from .services import whatsapp_service

    try:
        inquiry = VisitorInquiry.objects.get(id=inquiry_id)

        # Send to community WhatsApp
        community_phone = settings.WHATSAPP_COMMUNITY_NUMBER
        message = whatsapp_service.format_inquiry_message(inquiry)

        success = whatsapp_service.send_message(
            to_phone=community_phone,
            message=message,
            inquiry=inquiry
        )

        if success:
            inquiry.whatsapp_notified = True
            inquiry.save(update_fields=["whatsapp_notified"])
            logger.info(f"WhatsApp notification sent for inquiry {inquiry_id}")

    except VisitorInquiry.DoesNotExist:
        logger.error(f"Inquiry {inquiry_id} not found")

    except Exception as e:
        logger.error(f"WhatsApp notification failed: {str(e)}")
        self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_visitor_confirmation_email(self, inquiry_id: int):
    """
    Send confirmation email to the visitor.
    """
    from apps.visitors.models import VisitorInquiry
    from .services import email_service

    try:
        inquiry = VisitorInquiry.objects.get(id=inquiry_id)
        email_service.send_visitor_confirmation(inquiry)
        logger.info(f"Visitor confirmation sent for inquiry {inquiry_id}")

    except VisitorInquiry.DoesNotExist:
        logger.error(f"Inquiry {inquiry_id} not found")

    except Exception as e:
        logger.error(f"Visitor confirmation failed: {str(e)}")
        self.retry(exc=e, countdown=60)
