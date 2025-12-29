"""
Category management views
"""
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from apps.management.mixins import StaffRequiredMixin
from apps.news.models import Category


class CategoryListView(StaffRequiredMixin, ListView):
    """รายการหมวดหมู่ข่าว"""
    model = Category
    template_name = 'management/categories/list.html'
    context_object_name = 'categories'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'จัดการหมวดหมู่ข่าว'
        return context


class CategoryCreateView(StaffRequiredMixin, CreateView):
    """สร้างหมวดหมู่ข่าวใหม่"""
    model = Category
    template_name = 'management/categories/form.html'
    fields = ['name', 'slug', 'color']
    success_url = reverse_lazy('management:category_list')

    def form_valid(self, form):
        messages.success(self.request, f'เพิ่มหมวดหมู่ "{form.instance.name}" สำเร็จ')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'เพิ่มหมวดหมู่ข่าวใหม่'
        context['submit_text'] = 'เพิ่มหมวดหมู่'
        return context


class CategoryUpdateView(StaffRequiredMixin, UpdateView):
    """แก้ไขหมวดหมู่ข่าว"""
    model = Category
    template_name = 'management/categories/form.html'
    fields = ['name', 'slug', 'color']
    success_url = reverse_lazy('management:category_list')

    def form_valid(self, form):
        messages.success(self.request, f'แก้ไขหมวดหมู่ "{form.instance.name}" สำเร็จ')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'แก้ไขหมวดหมู่: {self.object.name}'
        context['submit_text'] = 'บันทึกการแก้ไข'
        return context


class CategoryDeleteView(StaffRequiredMixin, DeleteView):
    """ลบหมวดหมู่ข่าว"""
    model = Category
    template_name = 'management/categories/delete.html'
    success_url = reverse_lazy('management:category_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, f'ลบหมวดหมู่ "{obj.name}" สำเร็จ')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'ยืนยันการลบหมวดหมู่'
        # Count news in this category
        context['news_count'] = self.object.news_set.count()
        return context
