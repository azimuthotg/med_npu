from django.views.generic import TemplateView, ListView
from .models import Executive, Department


class AboutIndexView(TemplateView):
    """หน้าเกี่ยวกับคณะ"""
    template_name = 'about/index.html'


class HistoryView(TemplateView):
    """หน้าประวัติความเป็นมา"""
    template_name = 'about/history.html'


class VisionMissionView(TemplateView):
    """หน้าวิสัยทัศน์/พันธกิจ"""
    template_name = 'about/vision_mission.html'


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


class OrganizationView(TemplateView):
    """หน้าโครงสร้างองค์กร"""
    template_name = 'about/organization.html'


# ========================================
# Personnel Views
# ========================================

class PersonnelIndexView(TemplateView):
    """หน้าบุคลากร - Landing Page"""
    template_name = 'about/personnel/index.html'


class PersonnelPreclinicalView(TemplateView):
    """บุคลากรชั้นปรีคลินิก"""
    template_name = 'about/personnel/preclinical.html'


class PersonnelClinicalView(TemplateView):
    """บุคลากรชั้นคลินิก"""
    template_name = 'about/personnel/clinical.html'


class PersonnelThaiMedicineView(TemplateView):
    """แพทย์ไทยประยุกต์"""
    template_name = 'about/personnel/thai_medicine.html'


class PersonnelSupportingStaffView(TemplateView):
    """บุคลากรสายสนับสนุน"""
    template_name = 'about/personnel/supporting_staff.html'


class FacultyBoardView(TemplateView):
    """คณะกรรมการประจำคณะ"""
    template_name = 'about/faculty_board.html'
