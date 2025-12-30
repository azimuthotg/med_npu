"""
Personnel management views
"""
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from apps.management.mixins import ExecutivePermissionMixin
from apps.about.models import Personnel, Department


class PersonnelListView(ExecutivePermissionMixin, ListView):
    """รายการบุคลากร"""
    model = Personnel
    template_name = 'management/personnel/list.html'
    context_object_name = 'personnel_list'
    paginate_by = 30
    ordering = ['personnel_type', 'order', 'first_name']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Search
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(title__icontains=search_query) |
                Q(position__icontains=search_query) |
                Q(specialization__icontains=search_query)
            )

        # Filter by personnel type
        personnel_type = self.request.GET.get('personnel_type', '').strip()
        if personnel_type:
            queryset = queryset.filter(personnel_type=personnel_type)

        # Filter by department
        department_id = self.request.GET.get('department', '').strip()
        if department_id:
            queryset = queryset.filter(department_id=department_id)

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
        context['selected_personnel_type'] = self.request.GET.get('personnel_type', '')
        context['selected_department'] = self.request.GET.get('department', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['personnel_type_choices'] = Personnel.PERSONNEL_TYPE_CHOICES
        context['departments'] = Department.objects.filter(is_active=True).order_by('name')
        context['total_personnel'] = Personnel.objects.count()
        context['active_personnel'] = Personnel.objects.filter(is_active=True).count()

        # Count by type
        context['preclinical_count'] = Personnel.objects.filter(personnel_type='preclinical').count()
        context['clinical_count'] = Personnel.objects.filter(personnel_type='clinical').count()
        context['thai_medicine_count'] = Personnel.objects.filter(personnel_type='thai_medicine').count()
        context['supporting_count'] = Personnel.objects.filter(personnel_type='supporting_staff').count()

        return context


class PersonnelCreateView(ExecutivePermissionMixin, CreateView):
    """สร้างบุคลากรใหม่"""
    model = Personnel
    template_name = 'management/personnel/form.html'
    fields = [
        'title', 'first_name', 'last_name', 'personnel_type', 'position',
        'department', 'responsibilities', 'specialization', 'education', 'photo', 'email', 'phone',
        'order', 'is_active'
    ]
    success_url = reverse_lazy('management:personnel_list')

    def form_valid(self, form):
        messages.success(self.request, f'เพิ่มบุคลากร "{form.instance.full_name}" สำเร็จ')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'เพิ่มบุคลากรใหม่'
        context['submit_text'] = 'บันทึก'
        return context


class PersonnelUpdateView(ExecutivePermissionMixin, UpdateView):
    """แก้ไขข้อมูลบุคลากร"""
    model = Personnel
    template_name = 'management/personnel/form.html'
    fields = [
        'title', 'first_name', 'last_name', 'personnel_type', 'position',
        'department', 'responsibilities', 'specialization', 'education', 'photo', 'email', 'phone',
        'order', 'is_active'
    ]
    success_url = reverse_lazy('management:personnel_list')

    def form_valid(self, form):
        messages.success(self.request, f'แก้ไขข้อมูล "{form.instance.full_name}" สำเร็จ')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'แก้ไขข้อมูล: {self.object.full_name}'
        context['submit_text'] = 'บันทึกการแก้ไข'
        return context


class PersonnelDeleteView(ExecutivePermissionMixin, DeleteView):
    """ลบบุคลากร"""
    model = Personnel
    template_name = 'management/personnel/delete.html'
    success_url = reverse_lazy('management:personnel_list')

    def delete(self, request, *args, **kwargs):
        personnel_name = self.get_object().full_name
        messages.success(request, f'ลบข้อมูล "{personnel_name}" สำเร็จ')
        return super().delete(request, *args, **kwargs)
