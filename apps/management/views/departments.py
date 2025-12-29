"""
Department management views
"""
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from apps.management.mixins import ExecutivePermissionMixin
from apps.about.models import Department, Executive


class DepartmentListView(ExecutivePermissionMixin, ListView):
    """รายการภาควิชา"""
    model = Department
    template_name = 'management/departments/list.html'
    context_object_name = 'departments'
    paginate_by = 20
    ordering = ['order', 'name']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Search
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(name_en__icontains=search_query) |
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
        context['total_departments'] = Department.objects.count()
        context['active_departments'] = Department.objects.filter(is_active=True).count()
        return context


class DepartmentCreateView(ExecutivePermissionMixin, CreateView):
    """สร้างภาควิชาใหม่"""
    model = Department
    template_name = 'management/departments/form.html'
    fields = [
        'name', 'name_en', 'description', 'head',
        'phone', 'email', 'order', 'is_active'
    ]
    success_url = reverse_lazy('management:department_list')

    def form_valid(self, form):
        messages.success(self.request, f'เพิ่มภาควิชา "{form.instance.name}" สำเร็จ')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'เพิ่มภาควิชาใหม่'
        context['submit_text'] = 'บันทึก'
        return context


class DepartmentUpdateView(ExecutivePermissionMixin, UpdateView):
    """แก้ไขภาควิชา"""
    model = Department
    template_name = 'management/departments/form.html'
    fields = [
        'name', 'name_en', 'description', 'head',
        'phone', 'email', 'order', 'is_active'
    ]
    success_url = reverse_lazy('management:department_list')

    def form_valid(self, form):
        messages.success(self.request, f'แก้ไขภาควิชา "{form.instance.name}" สำเร็จ')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'แก้ไขภาควิชา: {self.object.name}'
        context['submit_text'] = 'บันทึกการแก้ไข'
        return context


class DepartmentDeleteView(ExecutivePermissionMixin, DeleteView):
    """ลบภาควิชา"""
    model = Department
    template_name = 'management/departments/delete.html'
    success_url = reverse_lazy('management:department_list')

    def delete(self, request, *args, **kwargs):
        department_name = self.get_object().name
        messages.success(request, f'ลบภาควิชา "{department_name}" สำเร็จ')
        return super().delete(request, *args, **kwargs)
