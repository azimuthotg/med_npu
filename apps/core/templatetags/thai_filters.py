from django import template
from datetime import datetime

register = template.Library()


@register.filter(name='thai_date')
def thai_date(value, format_type='short'):
    """
    แปลงวันที่เป็นภาษาไทย พ.ศ.

    Usage:
        {{ date|thai_date }}           → "29 ธ.ค. 2567"
        {{ date|thai_date:"full" }}    → "29 ธันวาคม 2567"
        {{ date|thai_date:"short" }}   → "29 ธ.ค. 2567"
    """
    if not value:
        return ""

    # ชื่อเดือนภาษาไทย (แบบเต็ม)
    thai_months_full = [
        '', 'มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน',
        'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม',
        'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'
    ]

    # ชื่อเดือนภาษาไทย (แบบย่อ)
    thai_months_short = [
        '', 'ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.',
        'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.',
        'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'
    ]

    try:
        if isinstance(value, str):
            date_obj = datetime.strptime(value, '%Y-%m-%d')
        else:
            date_obj = value

        day = date_obj.day
        month = date_obj.month
        year = date_obj.year + 543  # แปลง ค.ศ. เป็น พ.ศ.

        # เลือกชื่อเดือนตาม format_type
        if format_type == 'full':
            month_name = thai_months_full[month]
            return f"{day} {month_name} {year}"
        else:  # short
            month_name = thai_months_short[month]
            return f"{day} {month_name} {year}"

    except (ValueError, AttributeError):
        return str(value)


@register.filter(name='thai_date_long')
def thai_date_long(value):
    """
    แปลงวันที่เป็นภาษาไทยแบบยาว

    Usage:
        {{ date|thai_date_long }}  → "วันอาทิตย์ที่ 29 ธันวาคม พ.ศ. 2567"
    """
    if not value:
        return ""

    thai_days = [
        'จันทร์', 'อังคาร', 'พุธ', 'พฤหัสบดี',
        'ศุกร์', 'เสาร์', 'อาทิตย์'
    ]

    thai_months = [
        '', 'มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน',
        'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม',
        'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'
    ]

    try:
        if isinstance(value, str):
            date_obj = datetime.strptime(value, '%Y-%m-%d')
        else:
            date_obj = value

        day_name = thai_days[date_obj.weekday()]
        day = date_obj.day
        month = thai_months[date_obj.month]
        year = date_obj.year + 543

        return f"วัน{day_name}ที่ {day} {month} พ.ศ. {year}"

    except (ValueError, AttributeError):
        return str(value)
