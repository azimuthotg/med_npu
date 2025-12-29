"""
Popup management views
"""
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from apps.management.mixins import StaffRequiredMixin
from apps.core.models import Popup


class PopupListView(StaffRequiredMixin, ListView):
    """รายการ Popup ทั้งหมด"""
    model = Popup
    template_name = 'management/popups/list.html'
    context_object_name = 'popups'
    paginate_by = 20

    def get_queryset(self):
        queryset = Popup.objects.all()

        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
            )

        # Filter by status
        status = self.request.GET.get('status')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Statistics
        total_popups = Popup.objects.count()
        active_popups = Popup.objects.filter(is_active=True).count()

        # Sum analytics
        total_views = sum(p.view_count for p in Popup.objects.all())
        total_clicks = sum(p.click_count for p in Popup.objects.all())

        context['stats'] = {
            'total': total_popups,
            'active': active_popups,
            'inactive': total_popups - active_popups,
            'total_views': total_views,
            'total_clicks': total_clicks,
            'avg_ctr': round((total_clicks / total_views * 100), 2) if total_views > 0 else 0,
        }

        context['search'] = self.request.GET.get('search', '')
        context['status'] = self.request.GET.get('status', '')

        return context


class PopupCreateView(StaffRequiredMixin, CreateView):
    """สร้าง Popup ใหม่"""
    model = Popup
    template_name = 'management/popups/form.html'
    fields = [
        'title', 'image', 'link_url', 'link_text',
        'is_active', 'start_date', 'end_date',
        'show_frequency', 'show_delay', 'auto_close_delay', 'size'
    ]
    success_url = reverse_lazy('management:popup_list')

    def form_valid(self, form):
        messages.success(self.request, f'สร้าง Popup "{form.instance.title}" สำเร็จ')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'สร้าง Popup ใหม่'
        context['submit_text'] = 'สร้าง Popup'
        return context


class PopupUpdateView(StaffRequiredMixin, UpdateView):
    """แก้ไข Popup"""
    model = Popup
    template_name = 'management/popups/form.html'
    fields = [
        'title', 'image', 'link_url', 'link_text',
        'is_active', 'start_date', 'end_date',
        'show_frequency', 'show_delay', 'auto_close_delay', 'size'
    ]
    success_url = reverse_lazy('management:popup_list')

    def form_valid(self, form):
        messages.success(self.request, f'แก้ไข Popup "{form.instance.title}" สำเร็จ')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'แก้ไข Popup'
        context['submit_text'] = 'บันทึกการแก้ไข'
        return context


class PopupDeleteView(StaffRequiredMixin, DeleteView):
    """ลบ Popup"""
    model = Popup
    template_name = 'management/popups/delete.html'
    success_url = reverse_lazy('management:popup_list')

    def delete(self, request, *args, **kwargs):
        popup = self.get_object()
        messages.success(request, f'ลบ Popup "{popup.title}" สำเร็จ')
        return super().delete(request, *args, **kwargs)
