from django.views.generic import ListView, DetailView
from .models import Gallery


class GalleryListView(ListView):
    """รายการอัลบั้มทั้งหมด"""
    model = Gallery
    template_name = 'gallery/gallery_list.html'
    context_object_name = 'galleries'
    paginate_by = 12

    def get_queryset(self):
        return Gallery.objects.filter(is_published=True).prefetch_related('images')


class GalleryDetailView(DetailView):
    """รายละเอียดอัลบั้มและรูปภาพทั้งหมด"""
    model = Gallery
    template_name = 'gallery/gallery_detail.html'
    context_object_name = 'gallery'

    def get_queryset(self):
        return Gallery.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.images.all()
        return context
