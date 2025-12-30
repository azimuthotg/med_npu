"""
Responsibility management views
"""
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from apps.management.mixins import ExecutivePermissionMixin
from apps.about.models import Responsibility


class ResponsibilityListView(ExecutivePermissionMixin, ListView):
    """รายการหน้าที่ความรับผิดชอบ"""
    model = Responsibility
    template_name = 'management/responsibilities/list.html'
    context_object_name = 'responsibilities'
    paginate_by = 30
    ordering = ['order', 'name']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Search
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
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
        context['total_responsibilities'] = Responsibility.objects.count()
        context['active_responsibilities'] = Responsibility.objects.filter(is_active=True).count()
        return context


class ResponsibilityCreateView(ExecutivePermissionMixin, CreateView):
    """สร้างหน้าที่ใหม่"""
    model = Responsibility
    template_name = 'management/responsibilities/form.html'
    fields = ['name', 'description', 'order', 'is_active']
    success_url = reverse_lazy('management:responsibility_list')

    def form_valid(self, form):
        messages.success(self.request, f'เพิ่มหน้าที่ "{form.instance.name}" สำเร็จ')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'เพิ่มหน้าที่ใหม่'
        context['submit_text'] = 'บันทึก'
        return context


class ResponsibilityUpdateView(ExecutivePermissionMixin, UpdateView):
    """แก้ไขหน้าที่"""
    model = Responsibility
    template_name = 'management/responsibilities/form.html'
    fields = ['name', 'description', 'order', 'is_active']
    success_url = reverse_lazy('management:responsibility_list')

    def form_valid(self, form):
        messages.success(self.request, f'แก้ไขหน้าที่ "{form.instance.name}" สำเร็จ')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'แก้ไขหน้าที่: {self.object.name}'
        context['submit_text'] = 'บันทึกการแก้ไข'
        return context


class ResponsibilityDeleteView(ExecutivePermissionMixin, DeleteView):
    """ลบหน้าที่"""
    model = Responsibility
    template_name = 'management/responsibilities/delete.html'
    success_url = reverse_lazy('management:responsibility_list')

    def delete(self, request, *args, **kwargs):
        responsibility_name = self.get_object().name
        messages.success(request, f'ลบหน้าที่ "{responsibility_name}" สำเร็จ')
        return super().delete(request, *args, **kwargs)
