"""
Dashboard view for management panel
"""
from django.views.generic import TemplateView
from django.db.models import Count
from apps.management.mixins import StaffRequiredMixin
from apps.news.models import News
from apps.about.models import Executive, Department
from apps.education.models import Program, Admission


class DashboardView(StaffRequiredMixin, TemplateView):
    """หน้า Dashboard - แสดงสถิติและข้อมูลสรุป"""
    template_name = 'management/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # สถิติทั่วไป
        context['stats'] = {
            'news_count': News.objects.filter(is_published=True).count(),
            'news_draft_count': News.objects.filter(is_published=False).count(),
            'executives_count': Executive.objects.filter(is_active=True).count(),
            'departments_count': Department.objects.filter(is_active=True).count(),
            'programs_count': Program.objects.filter(is_active=True).count(),
            'admissions_open_count': Admission.objects.filter(is_active=True).count(),
        }

        # ข่าวล่าสุด 5 ข่าว
        context['latest_news'] = News.objects.order_by('-created_at')[:5]

        # ประกาศรับสมัครที่เปิดอยู่
        context['active_admissions'] = Admission.objects.filter(
            is_active=True
        ).order_by('-start_date')[:5]

        # ข่าวที่ดูมากที่สุด
        context['popular_news'] = News.objects.filter(
            is_published=True
        ).order_by('-view_count')[:5]

        return context
