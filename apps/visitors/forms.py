"""
Visitors forms - Main inquiry form
"""

import re

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import VisitorInquiry, ServiceChoice


class VisitorInquiryForm(forms.ModelForm):
    """
    Main visitor inquiry form.
    This is the central form that gates access to detailed information.
    """

    # Services as multiple checkboxes
    services = forms.MultipleChoiceField(
        choices=ServiceChoice.choices,
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "service-checkbox"}
        ),
        required=True,
        label=_("Servicios de interés"),
        help_text=_("Selecciona los servicios que te interesan")
    )

    # Privacy consent
    privacy_consent = forms.BooleanField(
        required=True,
        label=_("Acepto que mis datos sean utilizados para contactarme"),
        widget=forms.CheckboxInput(
            attrs={"class": "consent-checkbox"}
        )
    )

    class Meta:
        model = VisitorInquiry
        fields = [
            "full_name",
            "phone",
            "email",
            "city",
            "country",
            "estimated_arrival",
            "estimated_departure",
            "number_of_people",
            "number_of_children",
            "services",
            "special_requests",
        ]
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": _("Tu nombre completo"),
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": _("+57 300 123 4567"),
                    "type": "tel",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-input",
                    "placeholder": _("tu@correo.com"),
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": _("Bogotá, Cali, Medellín..."),
                }
            ),
            "country": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": _("Colombia"),
                }
            ),
            "estimated_arrival": forms.DateInput(
                attrs={
                    "class": "form-input",
                    "type": "date",
                }
            ),
            "estimated_departure": forms.DateInput(
                attrs={
                    "class": "form-input",
                    "type": "date",
                }
            ),
            "number_of_people": forms.NumberInput(
                attrs={
                    "class": "form-input",
                    "min": "1",
                    "max": "50",
                }
            ),
            "number_of_children": forms.NumberInput(
                attrs={
                    "class": "form-input",
                    "min": "0",
                    "max": "20",
                }
            ),
            "special_requests": forms.Textarea(
                attrs={
                    "class": "form-textarea",
                    "rows": 3,
                    "placeholder": _("¿Tienes alguna pregunta o necesidad especial?"),
                }
            ),
        }

    def clean_services(self):
        """Convert services to list for JSON storage."""
        services = self.cleaned_data.get("services", [])
        return list(services)

    def clean_phone(self):
        """Validate and clean phone number."""
        phone = self.cleaned_data.get("phone", "")
        # Remove spaces, dashes, and parentheses
        cleaned_phone = re.sub(r'[\s\-\(\)]', '', phone)
        # Validate format: optional + followed by 10-15 digits
        if not re.match(r'^\+?[0-9]{10,15}$', cleaned_phone):
            raise forms.ValidationError(
                _("Número de teléfono inválido. Usa formato: +57 300 123 4567")
            )
        return phone  # Return original format for readability

    def clean(self):
        """Validate dates."""
        cleaned_data = super().clean()
        arrival = cleaned_data.get("estimated_arrival")
        departure = cleaned_data.get("estimated_departure")

        if arrival and departure and departure < arrival:
            raise forms.ValidationError(
                _("La fecha de salida debe ser posterior a la fecha de llegada")
            )

        return cleaned_data
