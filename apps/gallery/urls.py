from django.urls import path, register_converter
from . import views


# Custom path converter for Unicode slugs (Thai language support)
class UnicodeSlugConverter:
    regex = r'[-\w]+'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


# Register the custom converter
register_converter(UnicodeSlugConverter, 'unicode_slug')

app_name = 'gallery'

urlpatterns = [
    path('', views.GalleryListView.as_view(), name='list'),
    path('<unicode_slug:slug>/', views.GalleryDetailView.as_view(), name='detail'),
]
