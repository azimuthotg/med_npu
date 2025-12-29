from django.views.generic import TemplateView
from apps.news.models import News
from apps.core.models import Banner, SiteSettings, Popup


class HomeView(TemplateView):
    """หน้าแรกของเว็บไซต์"""
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # โหลด SiteSettings และส่งไปที่ template
        try:
            site_settings = SiteSettings.load()
            context['site_settings'] = site_settings
            banner_enabled = site_settings.enable_banner
        except:
            context['site_settings'] = None
            banner_enabled = False

        # ดึงแบนเนอร์เฉพาะเมื่อเปิดใช้งาน
        if banner_enabled:
            try:
                all_banners = Banner.objects.filter(is_active=True).order_by('order')
                # กรองเฉพาะแบนเนอร์ที่ควรแสดงตามวันที่
                context['banners'] = [banner for banner in all_banners if banner.is_visible]
            except:
                context['banners'] = []
        else:
            context['banners'] = []

        # ดึงข่าวล่าสุด 3 ข่าว
        try:
            context['latest_news'] = News.objects.filter(
                is_published=True
            ).order_by('-published_at')[:3]
        except:
            context['latest_news'] = []

        # สถิติ
        context['stats'] = {
            'faculty': 50,
            'students': 300,
            'research': 100,
            'programs': 5,
        }

        # ดึง Popup ที่ active
        try:
            active_popup = Popup.objects.filter(is_active=True).first()
            if active_popup and active_popup.is_visible:
                context['popup'] = active_popup
        except:
            context['popup'] = None

        return context


class ContactView(TemplateView):
    """หน้าติดต่อเรา"""
    template_name = 'pages/contact.html'


class DownloadView(TemplateView):
    """ศูนย์การดาวน์โหลด"""
    template_name = 'pages/download.html'


class SearchView(TemplateView):
    """หน้าค้นหา"""
    template_name = 'pages/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        context['query'] = query

        if query:
            # TODO: เพิ่มการค้นหาจาก models ต่างๆ
            context['results'] = []

        return context


# ========================================
# Research & Academic Services Views
# ========================================

class ResearchServicesView(TemplateView):
    """หน้าหลักวิจัยและบริการวิชาการ"""
    template_name = 'pages/research_services.html'


# Research Section
class ResearchCentersView(TemplateView):
    """ศูนย์วิจัย"""
    template_name = 'pages/research_centers.html'


class ResearchProjectsView(TemplateView):
    """โครงการวิจัย"""
    template_name = 'pages/research_projects.html'


class PublicationsView(TemplateView):
    """ผลงานวิจัย"""
    template_name = 'pages/publications.html'


class ResearchEthicsView(TemplateView):
    """จริยธรรมการวิจัย"""
    template_name = 'pages/research_ethics.html'


# Services Section
class CommunityServicesView(TemplateView):
    """โครงการบริการชุมชน"""
    template_name = 'pages/community_services.html'


class TrainingCoursesView(TemplateView):
    """หลักสูตรฝึกอบรม"""
    template_name = 'pages/training_courses.html'


class CollaborationView(TemplateView):
    """ความร่วมมือทางวิชาการ"""
    template_name = 'pages/collaboration.html'


# ========================================
# Quality Assurance Views
# ========================================

class QAWFMEView(TemplateView):
    """หน้า WFME (World Federation for Medical Education)"""
    template_name = 'pages/qa_wfme.html'


class QAEdPExView(TemplateView):
    """หน้า EdPEx (Education Criteria for Performance Excellence)"""
    template_name = 'pages/qa_edpex.html'


class QAAUNQAView(TemplateView):
    """หน้า AUNQA (ASEAN University Network Quality Assurance)"""
    template_name = 'pages/qa_aunqa.html'


class QANPUQAView(TemplateView):
    """หน้า NPUQA (Nakhon Phanom University Quality Assurance)"""
    template_name = 'pages/qa_npuqa.html'
