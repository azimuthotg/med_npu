from django.views.generic import TemplateView, ListView, DetailView
from .models import Program, Admission


class EducationIndexView(TemplateView):
    """หน้าหลักการศึกษา"""
    template_name = 'education/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['programs'] = Program.objects.filter(is_active=True)
        context['open_admissions'] = Admission.objects.filter(is_active=True)[:5]
        return context


class ProgramListView(ListView):
    """รายการหลักสูตร"""
    model = Program
    template_name = 'education/program_list.html'
    context_object_name = 'programs'
    
    def get_queryset(self):
        queryset = Program.objects.filter(is_active=True)
        level = self.request.GET.get('level')
        if level:
            queryset = queryset.filter(level=level)
        return queryset


class ProgramDetailView(DetailView):
    """รายละเอียดหลักสูตร"""
    model = Program
    template_name = 'education/program_detail.html'
    context_object_name = 'program'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Related admissions
        context['admissions'] = Admission.objects.filter(
            program=self.object,
            is_active=True
        )
        return context


class AdmissionListView(ListView):
    """รายการประกาศรับสมัคร"""
    model = Admission
    template_name = 'education/admission_list.html'
    context_object_name = 'admissions'
    
    def get_queryset(self):
        return Admission.objects.filter(is_active=True).select_related('program')


class CalendarView(TemplateView):
    """ปฏิทินการศึกษา"""
    template_name = 'education/calendar.html'


class FoundationView(TemplateView):
    """มูลนิธิคณะแพทยศาสตร์"""
    template_name = 'education/foundation.html'


class ScholarshipView(TemplateView):
    """ทุนการศึกษา"""
    template_name = 'education/scholarship.html'
