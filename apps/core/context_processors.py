"""
Context processors for site-wide variables
"""
from django.conf import settings
from .models import SiteSettings


def site_settings(request):
    """
    เพิ่มตัวแปร site settings ให้ใช้ได้ทุก template
    ดึงข้อมูลจาก SiteSettings model (database) แทน hardcode
    """
    # ดึงข้อมูลจาก database
    site_config = SiteSettings.load()

    return {
        # ข้อมูลพื้นฐานจาก settings.py (ไม่ควรเปลี่ยนบ่อย)
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'คณะแพทยศาสตร์ มหาวิทยาลัยนครพนม'),
        'SITE_NAME_EN': getattr(settings, 'SITE_NAME_EN', 'Faculty of Medicine, NPU'),
        'SITE_SHORT_NAME': getattr(settings, 'SITE_SHORT_NAME', 'MED NPU'),
        'PRIMARY_COLOR': getattr(settings, 'PRIMARY_COLOR', '#229799'),

        # ข้อมูลที่ดึงจาก database (แก้ไขได้ผ่าน Admin)
        'SITE_DESCRIPTION': site_config.site_description or getattr(settings, 'SITE_DESCRIPTION', ''),
        'CONTACT_EMAIL': site_config.contact_email or getattr(settings, 'CONTACT_EMAIL', ''),
        'CONTACT_PHONE': site_config.contact_phone or getattr(settings, 'CONTACT_PHONE', ''),
        'CONTACT_ADDRESS': site_config.contact_address or getattr(settings, 'CONTACT_ADDRESS', ''),
        'GOOGLE_MAPS_EMBED': site_config.google_maps_embed,
        'SOCIAL_FACEBOOK': site_config.facebook_url or getattr(settings, 'SOCIAL_FACEBOOK', ''),
        'SOCIAL_YOUTUBE': site_config.youtube_url or getattr(settings, 'SOCIAL_YOUTUBE', ''),
        'SOCIAL_LINE': site_config.line_id or getattr(settings, 'SOCIAL_LINE', ''),

        # ส่ง SiteSettings object ทั้งหมด (สำหรับหน้า home)
        'site_settings': site_config,
    }
