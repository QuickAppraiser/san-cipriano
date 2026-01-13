"""
Content models - Static content and biodiversity entries
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel


class BiodiversityCategory(models.TextChoices):
    """Categories for biodiversity entries."""
    BIRDS = "aves", _("Aves")
    AMPHIBIANS = "anfibios", _("Anfibios")
    MAMMALS = "mamiferos", _("Mamíferos")
    REPTILES = "reptiles", _("Reptiles")
    FISH = "peces", _("Peces")
    INSECTS = "insectos", _("Insectos")
    FLORA = "flora", _("Flora")


class BiodiversityEntry(TimeStampedModel):
    """
    Biodiversity entries for educational content.
    """

    name = models.CharField(_("nombre común"), max_length=100)
    scientific_name = models.CharField(
        _("nombre científico"),
        max_length=150,
        blank=True
    )
    category = models.CharField(
        _("categoría"),
        max_length=20,
        choices=BiodiversityCategory.choices
    )
    description = models.TextField(_("descripción"))
    conservation_status = models.CharField(
        _("estado de conservación"),
        max_length=100,
        blank=True,
        help_text=_("Ej: En peligro, Vulnerable, Preocupación menor")
    )
    image = models.ImageField(
        _("imagen"),
        upload_to="biodiversity/",
        null=True,
        blank=True
    )
    is_featured = models.BooleanField(_("destacado"), default=False)
    is_active = models.BooleanField(_("activo"), default=True)

    class Meta:
        verbose_name = _("Entrada de Biodiversidad")
        verbose_name_plural = _("Entradas de Biodiversidad")
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Experience(TimeStampedModel):
    """
    Natural experiences available in San Cipriano.
    """

    name = models.CharField(_("nombre"), max_length=100)
    description = models.TextField(_("descripción"))
    duration_info = models.CharField(
        _("información de duración"),
        max_length=100,
        blank=True,
        help_text=_("Ej: 'Medio día', '2-3 horas', 'Día completo'")
    )
    difficulty = models.CharField(
        _("dificultad"),
        max_length=50,
        blank=True,
        help_text=_("Ej: 'Fácil', 'Moderado', 'Exigente'")
    )
    icon = models.CharField(
        _("ícono"),
        max_length=10,
        default="🌿",
        help_text=_("Emoji representativo")
    )
    image = models.ImageField(
        _("imagen"),
        upload_to="experiences/",
        null=True,
        blank=True
    )
    is_featured = models.BooleanField(_("destacado"), default=False)
    is_active = models.BooleanField(_("activo"), default=True)
    order = models.PositiveIntegerField(_("orden"), default=0)

    class Meta:
        verbose_name = _("Experiencia")
        verbose_name_plural = _("Experiencias")
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class GalleryImage(TimeStampedModel):
    """
    Gallery images for the site.
    """

    title = models.CharField(_("título"), max_length=100)
    description = models.TextField(_("descripción"), blank=True)
    image = models.ImageField(_("imagen"), upload_to="gallery/")
    is_hero = models.BooleanField(
        _("imagen hero"),
        default=False,
        help_text=_("Usar como imagen principal en el hero")
    )
    is_active = models.BooleanField(_("activo"), default=True)
    order = models.PositiveIntegerField(_("orden"), default=0)

    class Meta:
        verbose_name = _("Imagen de Galería")
        verbose_name_plural = _("Imágenes de Galería")
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title


class FAQ(TimeStampedModel):
    """
    Frequently asked questions.
    """

    question = models.CharField(_("pregunta"), max_length=300)
    answer = models.TextField(_("respuesta"))
    is_active = models.BooleanField(_("activo"), default=True)
    order = models.PositiveIntegerField(_("orden"), default=0)

    class Meta:
        verbose_name = _("Pregunta Frecuente")
        verbose_name_plural = _("Preguntas Frecuentes")
        ordering = ["order", "question"]

    def __str__(self):
        return self.question[:80]
