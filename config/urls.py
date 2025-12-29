"""
URL configuration for med_npu project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from apps.core import api_views

# Admin customization
admin.site.site_header = 'ระบบจัดการเว็บไซต์คณะแพทยศาสตร์'
admin.site.site_title = 'MED NPU Admin'
admin.site.index_title = 'แผงควบคุม'

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Management Panel (Custom Admin)
    path('manage/', include('apps.management.urls')),

    # API
    path('api/popup/<int:popup_id>/view/', api_views.popup_increment_view, name='popup_increment_view'),
    path('api/popup/<int:popup_id>/click/', api_views.popup_increment_click, name='popup_increment_click'),

    # Apps
    path('', include('apps.core.urls')),
    path('about/', include('apps.about.urls')),
    path('education/', include('apps.education.urls')),
    path('news/', include('apps.news.urls')),
    path('gallery/', include('apps.gallery.urls')),

    # Sitemap
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]

# Debug toolbar - uncomment when needed
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Static files served automatically by Django in DEBUG mode from STATICFILES_DIRS

    # try:
    #     import debug_toolbar
    #     urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    # except ImportError:
    #     pass
