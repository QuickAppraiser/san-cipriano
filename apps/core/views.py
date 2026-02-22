"""
Core views - Homepage and main pages
"""

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

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


class RobotsTxtView(View):
    """
    robots.txt for SEO - tells search engines what to crawl.
    """

    def get(self, request):
        protocol = "https" if request.is_secure() else "http"
        host = request.get_host()
        sitemap_url = f"{protocol}://{host}/sitemap.xml"

        content = f"""# robots.txt for San Cipriano - Community Tourism Website
# https://sancipriano.pythonanywhere.com

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


class GoogleVerificationView(View):
    """
    Google Search Console verification file.
    Replace GOOGLE_VERIFICATION_CODE with your actual code from Google Search Console.
    """

    def get(self, request, verification_code):
        # Google expects the file to contain: google-site-verification: googleXXXXXXXXXXXX.html
        content = f"google-site-verification: {verification_code}.html"
        return HttpResponse(content, content_type="text/html")


class BingSiteAuthView(View):
    """
    Bing Webmaster Tools verification file.
    """

    def get(self, request):
        content = """<?xml version="1.0"?>
<users>
	<user>302923EC95C786683432ED786D51C3FF</user>
</users>"""
        return HttpResponse(content, content_type="application/xml")


class SitemapView(View):
    """
    XML Sitemap for SEO - lists all public pages.
    """

    def get(self, request):
        from datetime import date
        # Build base URL
        protocol = "https" if request.is_secure() else "http"
        host = request.get_host()
        base_url = f"{protocol}://{host}"
        today = date.today().isoformat()

        # Define all pages with their priorities and change frequencies
        pages = [
            {"url": "/", "priority": "1.0", "changefreq": "weekly", "lastmod": today},
            {"url": "/contenido/sobre-nosotros/", "priority": "0.9", "changefreq": "monthly", "lastmod": today},
            {"url": "/visitantes/servicios/", "priority": "0.9", "changefreq": "weekly", "lastmod": today},
            {"url": "/contenido/biodiversidad/", "priority": "0.8", "changefreq": "monthly", "lastmod": today},
            {"url": "/proteccion/", "priority": "0.8", "changefreq": "monthly", "lastmod": today},
            {"url": "/seguridad/", "priority": "0.8", "changefreq": "monthly", "lastmod": today},
            {"url": "/visitantes/consulta/", "priority": "0.9", "changefreq": "monthly", "lastmod": today},
            {"url": "/contenido/preguntas-frecuentes/", "priority": "0.7", "changefreq": "monthly", "lastmod": today},
            {"url": "/visitantes/contacto/", "priority": "0.7", "changefreq": "monthly", "lastmod": today},
            {"url": "/terminos/", "priority": "0.5", "changefreq": "yearly", "lastmod": "2026-01-01"},
            {"url": "/privacidad/", "priority": "0.5", "changefreq": "yearly", "lastmod": "2026-01-01"},
            {"url": "/cookies/", "priority": "0.3", "changefreq": "yearly", "lastmod": "2026-01-01"},
        ]

        # Supported languages for hreflang
        languages = ["es", "en", "fr", "de", "it", "pt"]

        # Build XML with xhtml namespace for hreflang
        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'

        for page in pages:
            xml_content += "  <url>\n"
            xml_content += f"    <loc>{base_url}{page['url']}</loc>\n"
            xml_content += f"    <lastmod>{page['lastmod']}</lastmod>\n"
            xml_content += f"    <changefreq>{page['changefreq']}</changefreq>\n"
            xml_content += f"    <priority>{page['priority']}</priority>\n"
            # Add hreflang alternates for each page
            for lang in languages:
                xml_content += f'    <xhtml:link rel="alternate" hreflang="{lang}" href="{base_url}/{lang}{page["url"]}"/>\n'
            xml_content += f'    <xhtml:link rel="alternate" hreflang="x-default" href="{base_url}{page["url"]}"/>\n'
            xml_content += "  </url>\n"

        xml_content += "</urlset>"

        return HttpResponse(xml_content, content_type="application/xml")
