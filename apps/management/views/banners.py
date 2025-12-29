"""
Banner management views
"""
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from apps.management.mixins import BannerPermissionMixin
from apps.core.models import Banner


class BannerListView(BannerPermissionMixin, ListView):
    """รายการแบนเนอร์ทั้งหมด"""
    model = Banner
    template_name = 'management/banners/list.html'
    context_object_name = 'banners'
    paginate_by = 20
    ordering = ['order', '-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Search
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        # Filter by status
        status = self.request.GET.get('status', '').strip()
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_status'] = self.request.GET.get('status', '')

        # Statistics
        context['total_banners'] = Banner.objects.count()
        context['active_banners'] = Banner.objects.filter(is_active=True).count()
        context['inactive_banners'] = Banner.objects.filter(is_active=False).count()

        return context


class BannerCreateView(BannerPermissionMixin, CreateView):
    """สร้างแบนเนอร์ใหม่"""
    model = Banner
    template_name = 'management/banners/form.html'
    fields = [
        'title', 'description', 'image',
        'button_text', 'button_link',
        'order', 'is_active',
        'start_date', 'end_date'
    ]
    success_url = reverse_lazy('management:banner_list')

    def form_valid(self, form):
        messages.success(self.request, f'สร้างแบนเนอร์ "{form.instance.title}" สำเร็จ')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'สร้างแบนเนอร์ใหม่'
        context['submit_text'] = 'บันทึกแบนเนอร์'
        return context


class BannerUpdateView(BannerPermissionMixin, UpdateView):
    """แก้ไขแบนเนอร์"""
    model = Banner
    template_name = 'management/banners/form.html'
    fields = [
        'title', 'description', 'image',
        'button_text', 'button_link',
        'order', 'is_active',
        'start_date', 'end_date'
    ]
    success_url = reverse_lazy('management:banner_list')

    def form_valid(self, form):
        messages.success(self.request, f'แก้ไขแบนเนอร์ "{form.instance.title}" สำเร็จ')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'แก้ไขแบนเนอร์: {self.object.title}'
        context['submit_text'] = 'บันทึกการแก้ไข'
        return context


class BannerDeleteView(BannerPermissionMixin, DeleteView):
    """ลบแบนเนอร์"""
    model = Banner
    template_name = 'management/banners/delete.html'
    success_url = reverse_lazy('management:banner_list')

    def delete(self, request, *args, **kwargs):
        banner_title = self.get_object().title
        messages.success(request, f'ลบแบนเนอร์ "{banner_title}" สำเร็จ')
        return super().delete(request, *args, **kwargs)
