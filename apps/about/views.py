from django.views.generic import TemplateView, ListView
from .models import Executive, Department, Personnel


class AboutIndexView(TemplateView):
    """หน้าเกี่ยวกับคณะ"""
    template_name = 'about/index.html'


class HistoryView(TemplateView):
    """หน้าประวัติความเป็นมา"""
    template_name = 'about/history.html'


class VisionMissionView(TemplateView):
    """หน้าวิสัยทัศน์/พันธกิจ"""
    template_name = 'about/vision_mission.html'


class DeanMessageView(TemplateView):
    """หน้าสารจากคณบดี"""
    template_name = 'about/dean_message.html'


class AnnualReportView(TemplateView):
    """หน้ารายงานประจำปี"""
    template_name = 'about/annual_report.html'


class ExecutivesView(ListView):
    """หน้าผู้บริหาร"""
    model = Executive
    template_name = 'about/executives.html'
    context_object_name = 'executives'
    
    def get_queryset(self):
        return Executive.objects.filter(is_active=True).order_by('order')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Group by position
        context['dean'] = self.get_queryset().filter(position='dean')
        context['vice_deans'] = self.get_queryset().filter(position='vice_dean')
        context['assistant_deans'] = self.get_queryset().filter(position='assistant_dean')
        return context


class DepartmentsView(ListView):
    """หน้าภาควิชา"""
    model = Department
    template_name = 'about/departments.html'
    context_object_name = 'departments'

    def get_queryset(self):
        return Department.objects.filter(is_active=True).order_by('order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Group departments by type
        context['preclinical_depts'] = self.get_queryset().filter(department_type='preclinical')
        context['clinical_depts'] = self.get_queryset().filter(department_type='clinical')
        context['thai_medicine_depts'] = self.get_queryset().filter(department_type='thai_medicine')
        return context


class OrganizationView(TemplateView):
    """หน้าโครงสร้างองค์กร"""
    template_name = 'about/organization.html'


# ========================================
# Personnel Views
# ========================================

class PersonnelIndexView(TemplateView):
    """หน้าบุคลากร - Landing Page"""
    template_name = 'about/personnel/index.html'


class PersonnelPreclinicalView(ListView):
    """บุคลากรชั้นปรีคลินิก"""
    model = Personnel
    template_name = 'about/personnel/preclinical.html'
    context_object_name = 'personnel_list'

    def get_queryset(self):
        return Personnel.objects.filter(
            personnel_type='preclinical',
            is_active=True
        ).order_by('order')


class PersonnelClinicalView(ListView):
    """บุคลากรชั้นคลินิก"""
    model = Personnel
    template_name = 'about/personnel/clinical.html'
    context_object_name = 'personnel_list'

    def get_queryset(self):
        return Personnel.objects.filter(
            personnel_type='clinical',
            is_active=True
        ).order_by('order')


class PersonnelThaiMedicineView(ListView):
    """แพทย์ไทยประยุกต์"""
    model = Personnel
    template_name = 'about/personnel/thai_medicine.html'
    context_object_name = 'personnel_list'

    def get_queryset(self):
        return Personnel.objects.filter(
            personnel_type='thai_medicine',
            is_active=True
        ).order_by('order')


class PersonnelSupportingStaffView(ListView):
    """บุคลากรสายสนับสนุน"""
    model = Personnel
    template_name = 'about/personnel/supporting_staff.html'
    context_object_name = 'personnel_list'

    def get_queryset(self):
        return Personnel.objects.filter(
            personnel_type='supporting_staff',
            is_active=True
        ).select_related('department', 'department__head').order_by('department__order', 'order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all support departments with their heads
        support_departments = Department.objects.filter(
            department_type='support',
            is_active=True
        ).select_related('head').order_by('order')

        # Group personnel by department
        departments_with_personnel = []
        for dept in support_departments:
            personnel = self.get_queryset().filter(department=dept)
            departments_with_personnel.append({
                'department': dept,
                'personnel': personnel,
                'count': personnel.count()
            })

        context['departments_with_personnel'] = departments_with_personnel
        context['support_departments'] = support_departments

        return context


class FacultyBoardView(TemplateView):
    """คณะกรรมการประจำคณะ"""
    template_name = 'about/faculty_board.html'
