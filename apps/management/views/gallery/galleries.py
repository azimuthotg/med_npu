from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from apps.gallery.models import Gallery
from apps.management.mixins import StaffRequiredMixin


class GalleryListView(StaffRequiredMixin, ListView):
    """รายการอัลบั้มทั้งหมด"""
    model = Gallery
    template_name = 'management/gallery/list.html'
    context_object_name = 'galleries'
    paginate_by = 20

    def get_queryset(self):
        return Gallery.objects.all().prefetch_related('images')


class GalleryCreateView(StaffRequiredMixin, CreateView):
    """สร้างอัลบั้มใหม่"""
    model = Gallery
    template_name = 'management/gallery/form.html'
    fields = ['title', 'description', 'cover_image', 'event_date', 'is_published', 'order']
    success_url = reverse_lazy('management:gallery_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'เพิ่มอัลบั้มใหม่'
        context['submit_text'] = 'สร้างอัลบั้ม'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'สร้างอัลบั้มเรียบร้อยแล้ว')
        return super().form_valid(form)


class GalleryUpdateView(StaffRequiredMixin, UpdateView):
    """แก้ไขอัลบั้ม"""
    model = Gallery
    template_name = 'management/gallery/form.html'
    fields = ['title', 'description', 'cover_image', 'event_date', 'is_published', 'order']
    success_url = reverse_lazy('management:gallery_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'แก้ไขอัลบั้ม: {self.object.title}'
        context['submit_text'] = 'บันทึกการแก้ไข'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'บันทึกการแก้ไขเรียบร้อยแล้ว')
        return super().form_valid(form)


class GalleryDeleteView(StaffRequiredMixin, DeleteView):
    """ลบอัลบั้ม"""
    model = Gallery
    template_name = 'management/gallery/delete.html'
    success_url = reverse_lazy('management:gallery_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'ลบอัลบั้ม'
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(request, f'ลบอัลบั้ม "{self.get_object().title}" เรียบร้อยแล้ว')
        return super().delete(request, *args, **kwargs)
