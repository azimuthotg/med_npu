"""
API views for Popup analytics
"""
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from apps.core.models import Popup


@require_POST
def popup_increment_view(request, popup_id):
    """เพิ่มจำนวนครั้งที่แสดง Popup"""
    try:
        popup = Popup.objects.get(pk=popup_id)
        popup.increment_view()
        return JsonResponse({'success': True, 'view_count': popup.view_count})
    except Popup.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Popup not found'}, status=404)


@require_POST
def popup_increment_click(request, popup_id):
    """เพิ่มจำนวนครั้งที่คลิกลิงก์ใน Popup"""
    try:
        popup = Popup.objects.get(pk=popup_id)
        popup.increment_click()
        return JsonResponse({'success': True, 'click_count': popup.click_count})
    except Popup.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Popup not found'}, status=404)
