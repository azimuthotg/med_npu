"""
Site Settings management views
"""
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from apps.management.mixins import StaffRequiredMixin
from apps.core.models import SiteSettings


class SiteSettingsView(StaffRequiredMixin, UpdateView):
    """จัดการตั้งค่าเว็บไซต์"""
    model = SiteSettings
    template_name = 'management/settings/form.html'
    fields = [
        'site_name',
        'site_description',
        'enable_banner',
        'hero_tag_line',
        'hero_title',
        'hero_subtitle',
        'hero_description',
        'hero_button1_text',
        'hero_button1_link',
        'hero_button2_text',
        'hero_button2_link',
        'contact_email',
        'contact_phone',
        'contact_address',
        'google_maps_embed',
        'facebook_url',
        'youtube_url',
        'line_id',
    ]
    success_url = reverse_lazy('management:settings')

    def get_object(self, queryset=None):
        """ดึง SiteSettings instance (singleton)"""
        return SiteSettings.load()

    def form_valid(self, form):
        messages.success(self.request, 'บันทึกการตั้งค่าเว็บไซต์สำเร็จ')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'ตั้งค่าเว็บไซต์'
        context['submit_text'] = 'บันทึกการตั้งค่า'
        return context
