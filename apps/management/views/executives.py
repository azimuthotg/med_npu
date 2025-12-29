"""
Executive management views
"""
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from apps.management.mixins import ExecutivePermissionMixin
from apps.about.models import Executive


class ExecutiveListView(ExecutivePermissionMixin, ListView):
    """รายการผู้บริหาร"""
    model = Executive
    template_name = 'management/executives/list.html'
    context_object_name = 'executives'
    paginate_by = 20
    ordering = ['order', 'position']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Search
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(title__icontains=search_query) |
                Q(position_title__icontains=search_query)
            )

        # Filter by position
        position = self.request.GET.get('position', '').strip()
        if position:
            queryset = queryset.filter(position=position)

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
        context['selected_position'] = self.request.GET.get('position', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['position_choices'] = Executive.POSITION_CHOICES
        context['total_executives'] = Executive.objects.count()
        context['active_executives'] = Executive.objects.filter(is_active=True).count()
        return context


class ExecutiveCreateView(ExecutivePermissionMixin, CreateView):
    """สร้างผู้บริหารใหม่"""
    model = Executive
    template_name = 'management/executives/form.html'
    fields = [
        'title', 'first_name', 'last_name', 'position', 'position_title',
        'photo', 'email', 'phone', 'order', 'is_active'
    ]
    success_url = reverse_lazy('management:executive_list')

    def form_valid(self, form):
        messages.success(self.request, f'เพิ่มผู้บริหาร "{form.instance.full_name}" สำเร็จ')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'เพิ่มผู้บริหารใหม่'
        context['submit_text'] = 'บันทึก'
        return context


class ExecutiveUpdateView(ExecutivePermissionMixin, UpdateView):
    """แก้ไขข้อมูลผู้บริหาร"""
    model = Executive
    template_name = 'management/executives/form.html'
    fields = [
        'title', 'first_name', 'last_name', 'position', 'position_title',
        'photo', 'email', 'phone', 'order', 'is_active'
    ]
    success_url = reverse_lazy('management:executive_list')

    def form_valid(self, form):
        messages.success(self.request, f'แก้ไขข้อมูล "{form.instance.full_name}" สำเร็จ')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'แก้ไขข้อมูล: {self.object.full_name}'
        context['submit_text'] = 'บันทึกการแก้ไข'
        return context


class ExecutiveDeleteView(ExecutivePermissionMixin, DeleteView):
    """ลบผู้บริหาร"""
    model = Executive
    template_name = 'management/executives/delete.html'
    success_url = reverse_lazy('management:executive_list')

    def delete(self, request, *args, **kwargs):
        executive_name = self.get_object().full_name
        messages.success(request, f'ลบข้อมูล "{executive_name}" สำเร็จ')
        return super().delete(request, *args, **kwargs)
