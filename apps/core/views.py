"""
Core views - Homepage and main pages
"""

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, View

from apps.visitors.models import VisitorInquiry, VisitorCounter


class HomeView(TemplateView):
    """
    Homepage view with hero, welcome message, and main CTA.
    """

    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get visitor counter (handle case where table doesn't exist yet)
        try:
            counter = VisitorCounter.get_counter()
            context["visitor_count"] = counter.total_count
        except Exception:
            context["visitor_count"] = 180  # Default value

        return context


class ProtectionView(TemplateView):
    """
    Reserve protection rules and guidelines.
    """

    template_name = "core/protection.html"


class SafetyView(TemplateView):
    """
    Safety rules and important warnings.
    """

    template_name = "core/safety.html"


class TermsView(TemplateView):
    """
    Terms and conditions page - legal disclaimers and liability waivers.
    """

    template_name = "core/terms.html"


class PrivacyView(TemplateView):
    """
    Privacy policy page - data protection and user rights.
    """

    template_name = "core/privacy.html"


class CookiesView(TemplateView):
    """
    Cookie policy page - cookie usage and management.
    """

    template_name = "core/cookies.html"


class SitemapView(View):
    """
    XML Sitemap for SEO - lists all public pages.
    """

    def get(self, request):
        # Build base URL
        protocol = "https" if request.is_secure() else "http"
        host = request.get_host()
        base_url = f"{protocol}://{host}"

        # Define all pages with their priorities and change frequencies
        pages = [
            {"url": "/", "priority": "1.0", "changefreq": "weekly"},
            {"url": "/contenido/sobre-nosotros/", "priority": "0.9", "changefreq": "monthly"},
            {"url": "/visitantes/servicios/", "priority": "0.9", "changefreq": "monthly"},
            {"url": "/contenido/biodiversidad/", "priority": "0.8", "changefreq": "monthly"},
            {"url": "/proteccion/", "priority": "0.8", "changefreq": "monthly"},
            {"url": "/seguridad/", "priority": "0.8", "changefreq": "monthly"},
            {"url": "/visitantes/consulta/", "priority": "0.9", "changefreq": "monthly"},
            {"url": "/contenido/preguntas-frecuentes/", "priority": "0.7", "changefreq": "monthly"},
            {"url": "/visitantes/contacto/", "priority": "0.7", "changefreq": "monthly"},
            {"url": "/terminos/", "priority": "0.5", "changefreq": "yearly"},
            {"url": "/privacidad/", "priority": "0.5", "changefreq": "yearly"},
            {"url": "/cookies/", "priority": "0.3", "changefreq": "yearly"},
        ]

        # Build XML
        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

        for page in pages:
            xml_content += "  <url>\n"
            xml_content += f"    <loc>{base_url}{page['url']}</loc>\n"
            xml_content += f"    <changefreq>{page['changefreq']}</changefreq>\n"
            xml_content += f"    <priority>{page['priority']}</priority>\n"
            xml_content += "  </url>\n"

        xml_content += "</urlset>"

        return HttpResponse(xml_content, content_type="application/xml")


class RobotsTxtView(View):
    """
    robots.txt for SEO - tells search engines what to crawl.
    """

    def get(self, request):
        protocol = "https" if request.is_secure() else "http"
        host = request.get_host()
        sitemap_url = f"{protocol}://{host}/sitemap.xml"

        content = f"""# robots.txt for San Cipriano - Community Tourism Website
# https://sancipriano.co

User-agent: *
Allow: /

# Disallow admin and API paths
Disallow: /admin/
Disallow: /api/
Disallow: /__debug__/

# Sitemap location
Sitemap: {sitemap_url}

# Crawl-delay for respectful crawling
Crawl-delay: 1
"""
        return HttpResponse(content, content_type="text/plain")
