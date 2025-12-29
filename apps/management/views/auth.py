"""
Authentication views for management panel
"""
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, View


class ManagementLoginView(FormView):
    """หน้า Login สำหรับระบบจัดการ"""
    template_name = 'management/auth/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('management:dashboard')

    def dispatch(self, request, *args, **kwargs):
        # ถ้า login แล้ว redirect ไป dashboard
        if request.user.is_authenticated and request.user.is_staff:
            return redirect('management:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()

        # ตรวจสอบว่าเป็น staff หรือไม่
        if not user.is_staff:
            messages.error(self.request, 'คุณไม่มีสิทธิ์เข้าถึงระบบจัดการ')
            return self.form_invalid(form)

        login(self.request, user)
        messages.success(self.request, f'ยินดีต้อนรับ {user.get_full_name() or user.username}')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
        return super().form_invalid(form)


class ManagementLogoutView(View):
    """Logout"""
    def get(self, request):
        logout(request)
        messages.success(request, 'ออกจากระบบเรียบร้อยแล้ว')
        return redirect('management:login')

    def post(self, request):
        return self.get(request)
