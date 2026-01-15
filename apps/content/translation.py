"""
Model translations for Content app.
Enables multi-language support for database content.
"""

from modeltranslation.translator import translator, TranslationOptions

from .models import BiodiversityEntry, Experience, GalleryImage, FAQ


class BiodiversityEntryTranslationOptions(TranslationOptions):
    """Translation options for biodiversity entries."""
    fields = ('name', 'description', 'conservation_status')


class ExperienceTranslationOptions(TranslationOptions):
    """Translation options for experiences."""
    fields = ('name', 'description', 'duration_info', 'difficulty')


class GalleryImageTranslationOptions(TranslationOptions):
    """Translation options for gallery images."""
    fields = ('title', 'description')


class FAQTranslationOptions(TranslationOptions):
    """Translation options for FAQs."""
    fields = ('question', 'answer')


# Register translations
translator.register(BiodiversityEntry, BiodiversityEntryTranslationOptions)
translator.register(Experience, ExperienceTranslationOptions)
translator.register(GalleryImage, GalleryImageTranslationOptions)
translator.register(FAQ, FAQTranslationOptions)
