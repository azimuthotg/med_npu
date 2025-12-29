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

app_name = 'news'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='list'),
    path('category/<unicode_slug:category_slug>/', views.NewsListView.as_view(), name='category'),
    path('<unicode_slug:slug>/', views.NewsDetailView.as_view(), name='detail'),
]
