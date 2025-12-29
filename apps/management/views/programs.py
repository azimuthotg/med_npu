"""
Program management views
"""
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from apps.management.mixins import ProgramPermissionMixin
from apps.education.models import Program, Admission


class ProgramListView(ProgramPermissionMixin, ListView):
    """รายการหลักสูตร"""
    model = Program
    template_name = 'management/programs/list.html'
    context_object_name = 'programs'
    paginate_by = 20
    ordering = ['order', 'level', 'name']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Search
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(name_en__icontains=search_query) |
                Q(degree__icontains=search_query)
            )

        # Filter by level
        level = self.request.GET.get('level', '').strip()
        if level:
            queryset = queryset.filter(level=level)

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
        context['selected_level'] = self.request.GET.get('level', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['level_choices'] = Program.LEVEL_CHOICES
        context['total_programs'] = Program.objects.count()
        context['active_programs'] = Program.objects.filter(is_active=True).count()
        return context


class ProgramCreateView(ProgramPermissionMixin, CreateView):
    """สร้างหลักสูตรใหม่"""
    model = Program
    template_name = 'management/programs/form.html'
    fields = [
        'name', 'name_en', 'slug', 'level', 'degree', 'degree_en',
        'duration', 'description', 'curriculum_file', 'image',
        'is_active', 'order'
    ]
    success_url = reverse_lazy('management:program_list')

    def form_valid(self, form):
        messages.success(self.request, f'เพิ่มหลักสูตร "{form.instance.name}" สำเร็จ')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'เพิ่มหลักสูตรใหม่'
        context['submit_text'] = 'บันทึก'
        return context


class ProgramUpdateView(ProgramPermissionMixin, UpdateView):
    """แก้ไขหลักสูตร"""
    model = Program
    template_name = 'management/programs/form.html'
    fields = [
        'name', 'name_en', 'slug', 'level', 'degree', 'degree_en',
        'duration', 'description', 'curriculum_file', 'image',
        'is_active', 'order'
    ]
    success_url = reverse_lazy('management:program_list')

    def form_valid(self, form):
        messages.success(self.request, f'แก้ไขหลักสูตร "{form.instance.name}" สำเร็จ')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'แก้ไขหลักสูตร: {self.object.name}'
        context['submit_text'] = 'บันทึกการแก้ไข'
        return context


class ProgramDeleteView(ProgramPermissionMixin, DeleteView):
    """ลบหลักสูตร"""
    model = Program
    template_name = 'management/programs/delete.html'
    success_url = reverse_lazy('management:program_list')

    def delete(self, request, *args, **kwargs):
        program_name = self.get_object().name
        messages.success(request, f'ลบหลักสูตร "{program_name}" สำเร็จ')
        return super().delete(request, *args, **kwargs)


# Admission Management
class AdmissionListView(ProgramPermissionMixin, ListView):
    """รายการประกาศรับสมัคร"""
    model = Admission
    template_name = 'management/admissions/list.html'
    context_object_name = 'admissions'
    paginate_by = 20
    ordering = ['-academic_year', '-start_date']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Search
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(round_name__icontains=search_query)
            )

        # Filter by program
        program_id = self.request.GET.get('program', '').strip()
        if program_id:
            queryset = queryset.filter(program_id=program_id)

        # Filter by status
        status = self.request.GET.get('status', '').strip()
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['programs'] = Program.objects.filter(is_active=True)
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_program'] = self.request.GET.get('program', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['total_admissions'] = Admission.objects.count()
        context['active_admissions'] = Admission.objects.filter(is_active=True).count()
        return context


class AdmissionCreateView(ProgramPermissionMixin, CreateView):
    """สร้างประกาศรับสมัครใหม่"""
    model = Admission
    template_name = 'management/admissions/form.html'
    fields = [
        'title', 'program', 'academic_year', 'round_name',
        'start_date', 'end_date', 'quota', 'description',
        'requirements', 'announcement_file', 'apply_url', 'is_active'
    ]
    success_url = reverse_lazy('management:admission_list')

    def form_valid(self, form):
        messages.success(self.request, f'เพิ่มประกาศรับสมัคร "{form.instance.title}" สำเร็จ')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'เพิ่มประกาศรับสมัครใหม่'
        context['submit_text'] = 'บันทึก'
        return context


class AdmissionUpdateView(ProgramPermissionMixin, UpdateView):
    """แก้ไขประกาศรับสมัคร"""
    model = Admission
    template_name = 'management/admissions/form.html'
    fields = [
        'title', 'program', 'academic_year', 'round_name',
        'start_date', 'end_date', 'quota', 'description',
        'requirements', 'announcement_file', 'apply_url', 'is_active'
    ]
    success_url = reverse_lazy('management:admission_list')

    def form_valid(self, form):
        messages.success(self.request, f'แก้ไขประกาศรับสมัคร "{form.instance.title}" สำเร็จ')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'แก้ไขประกาศ: {self.object.title}'
        context['submit_text'] = 'บันทึกการแก้ไข'
        return context


class AdmissionDeleteView(ProgramPermissionMixin, DeleteView):
    """ลบประกาศรับสมัคร"""
    model = Admission
    template_name = 'management/admissions/delete.html'
    success_url = reverse_lazy('management:admission_list')

    def delete(self, request, *args, **kwargs):
        admission_title = self.get_object().title
        messages.success(request, f'ลบประกาศ "{admission_title}" สำเร็จ')
        return super().delete(request, *args, **kwargs)
