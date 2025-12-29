from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.db import models
from apps.gallery.models import Gallery, GalleryImage
from apps.management.mixins import StaffRequiredMixin


class GalleryImageManageView(StaffRequiredMixin, DetailView):
    """จัดการรูปภาพในอัลบั้ม"""
    model = Gallery
    template_name = 'management/gallery/images.html'
    context_object_name = 'gallery'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.images.all()
        return context


class GalleryImageCreateView(StaffRequiredMixin, CreateView):
    """เพิ่มรูปภาพในอัลบั้ม"""
    model = GalleryImage
    template_name = 'management/gallery/image_form.html'
    fields = ['image', 'caption', 'order']

    def dispatch(self, request, *args, **kwargs):
        self.gallery = get_object_or_404(Gallery, pk=kwargs['gallery_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery'] = self.gallery
        context['form_title'] = f'เพิ่มรูปภาพในอัลบั้ม: {self.gallery.title}'
        context['submit_text'] = 'อัปโหลดรูปภาพ'
        return context

    def form_valid(self, form):
        form.instance.gallery = self.gallery
        messages.success(self.request, 'เพิ่มรูปภาพเรียบร้อยแล้ว')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('management:gallery_images', kwargs={'pk': self.gallery.pk})


class GalleryImageUpdateView(StaffRequiredMixin, UpdateView):
    """แก้ไขข้อมูลรูปภาพ"""
    model = GalleryImage
    template_name = 'management/gallery/image_form.html'
    fields = ['caption', 'order']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery'] = self.object.gallery
        context['form_title'] = 'แก้ไขข้อมูลรูปภาพ'
        context['submit_text'] = 'บันทึกการแก้ไข'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'บันทึกการแก้ไขเรียบร้อยแล้ว')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('management:gallery_images', kwargs={'pk': self.object.gallery.pk})


class GalleryImageDeleteView(StaffRequiredMixin, DeleteView):
    """ลบรูปภาพ"""
    model = GalleryImage
    template_name = 'management/gallery/image_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery'] = self.object.gallery
        context['page_title'] = 'ลบรูปภาพ'
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'ลบรูปภาพเรียบร้อยแล้ว')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('management:gallery_images', kwargs={'pk': self.object.gallery.pk})


class GalleryBulkUploadView(StaffRequiredMixin, View):
    """อัปโหลดรูปภาพหลายไฟล์พร้อมกัน"""
    template_name = 'management/gallery/bulk_upload.html'

    def get(self, request, gallery_pk):
        gallery = get_object_or_404(Gallery, pk=gallery_pk)
        return render(request, self.template_name, {'gallery': gallery})

    def post(self, request, gallery_pk):
        gallery = get_object_or_404(Gallery, pk=gallery_pk)
        files = request.FILES.getlist('images')

        if not files:
            messages.error(request, 'กรุณาเลือกรูปภาพอย่างน้อย 1 รูป')
            return redirect('management:gallery_bulk_upload', gallery_pk=gallery.pk)

        # Get current max order
        max_order = gallery.images.aggregate(models.Max('order'))['order__max'] or 0

        # Upload all files
        uploaded_count = 0
        for index, file in enumerate(files):
            try:
                GalleryImage.objects.create(
                    gallery=gallery,
                    image=file,
                    order=max_order + index + 1
                )
                uploaded_count += 1
            except Exception as e:
                messages.warning(request, f'ไม่สามารถอัปโหลด {file.name}: {str(e)}')

        if uploaded_count > 0:
            messages.success(request, f'อัปโหลดรูปภาพสำเร็จ {uploaded_count} รูป')
        else:
            messages.error(request, 'ไม่สามารถอัปโหลดรูปภาพได้')

        return redirect('management:gallery_images', pk=gallery.pk)
