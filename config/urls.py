"""
URL configuration for San Cipriano project.
Sitio web oficial de la comunidad de San Cipriano, Colombia.
"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Admin customization
admin.site.site_header = "San Cipriano - Administración"
admin.site.site_title = "San Cipriano Admin"
admin.site.index_title = "Panel de Administración Comunitaria"

# Non-i18n URLs
urlpatterns = [
    # API Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    # API endpoints
    path("api/v1/visitors/", include("apps.visitors.api_urls")),
    path("api/v1/content/", include("apps.content.api_urls")),

    # Language switcher
    path("i18n/", include("django.conf.urls.i18n")),
]

# i18n URLs (with language prefix)
urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("visitantes/", include("apps.visitors.urls")),
    path("contenido/", include("apps.content.urls")),
    prefix_default_language=False,
)

# Debug toolbar (development only)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    try:
        import debug_toolbar
        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass
