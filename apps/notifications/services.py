"""
Notification services - WhatsApp and Email sending logic
"""

import logging
from datetime import datetime

import httpx
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from .models import NotificationLog, NotificationType, NotificationStatus

logger = logging.getLogger(__name__)


class WhatsAppService:
    """
    WhatsApp Business API integration service.
    Uses the official WhatsApp Cloud API.
    """

    def __init__(self):
        self.api_url = settings.WHATSAPP_API_URL
        self.api_token = settings.WHATSAPP_API_TOKEN
        self.phone_id = settings.WHATSAPP_PHONE_ID

    def is_configured(self):
        """Check if WhatsApp is properly configured."""
        return all([self.api_url, self.api_token, self.phone_id])

    def send_message(self, to_phone: str, message: str, inquiry=None) -> bool:
        """
        Send a WhatsApp message using the Cloud API.

        Args:
            to_phone: Recipient phone number (with country code)
            message: Message text to send
            inquiry: Optional VisitorInquiry instance for logging

        Returns:
            bool: True if message was sent successfully
        """
        # Create notification log
        log = NotificationLog.objects.create(
            notification_type=NotificationType.WHATSAPP,
            recipient=to_phone,
            message=message,
            inquiry=inquiry,
            status=NotificationStatus.PENDING,
        )

        if not self.is_configured():
            logger.warning("WhatsApp not configured, skipping notification")
            log.status = NotificationStatus.FAILED
            log.error_message = "WhatsApp API not configured"
            log.save()
            return False

        try:
            # Clean phone number
            clean_phone = to_phone.replace("+", "").replace(" ", "").replace("-", "")

            headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json",
            }

            payload = {
                "messaging_product": "whatsapp",
                "to": clean_phone,
                "type": "text",
                "text": {"body": message},
            }

            with httpx.Client() as client:
                response = client.post(
                    f"{self.api_url}/{self.phone_id}/messages",
                    headers=headers,
                    json=payload,
                    timeout=30,
                )
                response.raise_for_status()

            log.status = NotificationStatus.SENT
            log.sent_at = timezone.now()
            log.save()
            return True

        except httpx.HTTPStatusError as e:
            logger.error(f"WhatsApp API error: {e.response.text}")
            log.status = NotificationStatus.FAILED
            log.error_message = str(e.response.text)
            log.save()
            return False

        except Exception as e:
            logger.error(f"WhatsApp send error: {str(e)}")
            log.status = NotificationStatus.FAILED
            log.error_message = str(e)
            log.save()
            return False

    def format_inquiry_message(self, inquiry) -> str:
        """
        Format a visitor inquiry into a WhatsApp message.
        """
        services_list = ", ".join(inquiry.services_display) if inquiry.services else "No especificados"

        arrival = inquiry.estimated_arrival.strftime("%d/%m/%Y") if inquiry.estimated_arrival else "No especificada"
        departure = inquiry.estimated_departure.strftime("%d/%m/%Y") if inquiry.estimated_departure else "No especificada"

        message = f"""🌿 *Nueva Consulta de Visitante*

*Nombre:* {inquiry.full_name}
*Teléfono:* {inquiry.phone}
*Email:* {inquiry.email}
*Ciudad/País:* {inquiry.city}, {inquiry.country}

*Fechas:*
- Llegada: {arrival}
- Salida: {departure}

*Personas:* {inquiry.number_of_people} adultos, {inquiry.number_of_children} menores

*Servicios de interés:*
{services_list}

*Solicitudes especiales:*
{inquiry.special_requests or "Ninguna"}

---
Recibido: {inquiry.created_at.strftime("%d/%m/%Y %H:%M")}
"""
        return message


class EmailService:
    """
    Email notification service.
    """

    def send_inquiry_notification(self, inquiry) -> bool:
        """
        Send email notification about new visitor inquiry.
        """
        subject = f"Nueva consulta de {inquiry.full_name}"

        # Create notification log
        log = NotificationLog.objects.create(
            notification_type=NotificationType.EMAIL,
            recipient=settings.COMMUNITY_EMAIL,
            subject=subject,
            message="",  # Will be filled with HTML content
            inquiry=inquiry,
            status=NotificationStatus.PENDING,
        )

        try:
            # Render email template
            html_message = render_to_string(
                "emails/inquiry_notification.html",
                {"inquiry": inquiry}
            )
            plain_message = render_to_string(
                "emails/inquiry_notification.txt",
                {"inquiry": inquiry}
            )

            log.message = plain_message

            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.COMMUNITY_EMAIL],
                html_message=html_message,
                fail_silently=False,
            )

            log.status = NotificationStatus.SENT
            log.sent_at = timezone.now()
            log.save()

            # Update inquiry status
            inquiry.email_notified = True
            inquiry.save(update_fields=["email_notified"])

            return True

        except Exception as e:
            logger.error(f"Email send error: {str(e)}")
            log.status = NotificationStatus.FAILED
            log.error_message = str(e)
            log.save()
            return False

    def send_visitor_confirmation(self, inquiry) -> bool:
        """
        Send confirmation email to visitor.
        """
        subject = "¡Gracias por tu interés en San Cipriano!"

        log = NotificationLog.objects.create(
            notification_type=NotificationType.EMAIL,
            recipient=inquiry.email,
            subject=subject,
            message="",
            inquiry=inquiry,
            status=NotificationStatus.PENDING,
        )

        try:
            html_message = render_to_string(
                "emails/visitor_confirmation.html",
                {"inquiry": inquiry}
            )
            plain_message = render_to_string(
                "emails/visitor_confirmation.txt",
                {"inquiry": inquiry}
            )

            log.message = plain_message

            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[inquiry.email],
                html_message=html_message,
                fail_silently=False,
            )

            log.status = NotificationStatus.SENT
            log.sent_at = timezone.now()
            log.save()
            return True

        except Exception as e:
            logger.error(f"Visitor email error: {str(e)}")
            log.status = NotificationStatus.FAILED
            log.error_message = str(e)
            log.save()
            return False


# Service instances
whatsapp_service = WhatsAppService()
email_service = EmailService()
