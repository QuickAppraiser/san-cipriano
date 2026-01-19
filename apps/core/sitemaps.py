"""
Sitemaps for SEO - San Cipriano
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages."""
    priority = 0.8
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return [
            # Core pages
            'core:home',
            'core:protection',
            'core:safety',
            # Content pages - Explorar
            'content:places',
            'content:biodiversity',
            'content:education',
            'content:gastronomy',
            'content:photo_spots',
            'content:gallery',
            'content:map',
            # Content pages - Planificar
            'content:reservations',
            'content:itineraries',
            'content:packages',
            'content:prices',
            'content:how_to_get_there',
            'content:weather',
            'content:packing_list',
            'content:certified_guides',
            'content:safety',
            # Content pages - Conocenos
            'content:about',
            'content:history',
            'content:events',
            'content:testimonials',
            'content:faq',
            # Other
            'content:guides',
            'content:budget_calculator',
            'content:contact',
        ]

    def location(self, item):
        return reverse(item)


class HomeSitemap(Sitemap):
    """Sitemap for home page with highest priority."""
    priority = 1.0
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return ['core:home']

    def location(self, item):
        return reverse(item)
