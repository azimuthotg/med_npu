"""
Permission mixins for management app
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect


class StaffRequiredMixin(LoginRequiredMixin):
    """
    Mixin ที่ต้องการให้ user เป็น staff
    ใช้สำหรับทุก view ในระบบจัดการ
    """
    login_url = '/manage/login/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.is_staff:
            messages.error(request, 'คุณไม่มีสิทธิ์เข้าถึงระบบจัดการ')
            return redirect('core:home')

        return super().dispatch(request, *args, **kwargs)


class NewsPermissionMixin(StaffRequiredMixin):
    """Mixin สำหรับจัดการข่าว"""
    def dispatch(self, request, *args, **kwargs):
        # ตรวจสอบ permission (ถ้าต้องการ)
        # if not request.user.has_perm('news.change_news'):
        #     messages.error(request, 'คุณไม่มีสิทธิ์จัดการข่าว')
        #     return redirect('management:dashboard')
        return super().dispatch(request, *args, **kwargs)


class ExecutivePermissionMixin(StaffRequiredMixin):
    """Mixin สำหรับจัดการผู้บริหาร"""
    pass


class ProgramPermissionMixin(StaffRequiredMixin):
    """Mixin สำหรับจัดการหลักสูตร"""
    pass


class AdmissionPermissionMixin(StaffRequiredMixin):
    """Mixin สำหรับจัดการประกาศรับสมัคร"""
    pass


class BannerPermissionMixin(StaffRequiredMixin):
    """Mixin สำหรับจัดการแบนเนอร์"""
    pass
