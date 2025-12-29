from django.db import models


class TimeStampedModel(models.Model):
    """Abstract base model with timestamp fields"""
    created_at = models.DateTimeField('สร้างเมื่อ', auto_now_add=True)
    updated_at = models.DateTimeField('แก้ไขเมื่อ', auto_now=True)
    
    class Meta:
        abstract = True


class SiteSettings(models.Model):
    """Site-wide settings (Singleton)"""
    site_name = models.CharField('ชื่อเว็บไซต์', max_length=200, default='คณะแพทยศาสตร์')
    site_description = models.TextField('คำอธิบาย', blank=True)
    contact_email = models.EmailField('อีเมล', blank=True)
    contact_phone = models.CharField('โทรศัพท์', max_length=50, blank=True)
    contact_address = models.TextField('ที่อยู่', blank=True)
    google_maps_embed = models.TextField(
        'Google Maps Embed Code',
        blank=True,
        help_text='ใส่ iframe embed code จาก Google Maps (แชร์ > ฝังแผนที่)'
    )

    # Social Media
    facebook_url = models.URLField('Facebook', blank=True)
    youtube_url = models.URLField('YouTube', blank=True)
    line_id = models.CharField('Line ID', max_length=50, blank=True)

    # Banner Settings
    enable_banner = models.BooleanField(
        'เปิดใช้งานแบนเนอร์',
        default=False,
        help_text='เปิดเพื่อแสดง Carousel Banner / ปิดเพื่อแสดง Hero Section แบบเดิม'
    )

    # Hero Section Settings
    hero_tag_line = models.CharField(
        'Tag Line',
        max_length=200,
        default='🏥 ผลิตแพทย์เพื่อชุมชนอีสาน',
        blank=True
    )
    hero_title = models.CharField(
        'หัวข้อหลัก',
        max_length=200,
        default='คณะแพทยศาสตร์',
        blank=True
    )
    hero_subtitle = models.CharField(
        'หัวข้อย่อย',
        max_length=200,
        default='มหาวิทยาลัยนครพนม',
        blank=True
    )
    hero_description = models.TextField(
        'คำอธิบาย',
        default='มุ่งมั่นผลิตแพทย์ที่มีคุณภาพ เพื่อรับใช้สังคมและชุมชน',
        blank=True
    )
    hero_button1_text = models.CharField(
        'ปุ่มที่ 1 - ข้อความ',
        max_length=100,
        default='รับสมัครนักศึกษา',
        blank=True
    )
    hero_button1_link = models.CharField(
        'ปุ่มที่ 1 - ลิงก์',
        max_length=500,
        default='/education/admission/',
        blank=True
    )
    hero_button2_text = models.CharField(
        'ปุ่มที่ 2 - ข้อความ',
        max_length=100,
        default='เรียนรู้เพิ่มเติม',
        blank=True
    )
    hero_button2_link = models.CharField(
        'ปุ่มที่ 2 - ลิงก์',
        max_length=500,
        default='/about/',
        blank=True
    )

    class Meta:
        verbose_name = 'ตั้งค่าเว็บไซต์'
        verbose_name_plural = 'ตั้งค่าเว็บไซต์'
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Banner(TimeStampedModel):
    """แบนเนอร์/สไลด์หน้าแรก"""
    title = models.CharField('หัวข้อ', max_length=200)
    description = models.TextField('คำอธิบาย', blank=True)
    image = models.ImageField('รูปภาพ', upload_to='banners/%Y/%m/')

    # Call to Action
    button_text = models.CharField('ข้อความปุ่ม', max_length=100, blank=True)
    button_link = models.CharField('ลิงก์ปุ่ม', max_length=500, blank=True, help_text='URL เช่น /education/admission/ หรือ https://example.com')

    # Display Settings
    order = models.IntegerField('ลำดับการแสดง', default=0, help_text='เลขน้อยแสดงก่อน')
    is_active = models.BooleanField('เปิดใช้งาน', default=True)

    # Optional Date Range
    start_date = models.DateTimeField('วันที่เริ่มแสดง', null=True, blank=True)
    end_date = models.DateTimeField('วันที่สิ้นสุด', null=True, blank=True)

    class Meta:
        verbose_name = 'แบนเนอร์'
        verbose_name_plural = 'แบนเนอร์'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    @property
    def is_visible(self):
        """ตรวจสอบว่าแบนเนอร์ควรแสดงหรือไม่ตามวันที่"""
        if not self.is_active:
            return False

        from django.utils import timezone
        now = timezone.now()

        if self.start_date and now < self.start_date:
            return False

        if self.end_date and now > self.end_date:
            return False

        return True


class Popup(TimeStampedModel):
    """Pop-up/Modal โฆษณาหน้าแรก"""
    # Basic Info
    title = models.CharField('หัวข้อ', max_length=200)
    image = models.ImageField('รูปภาพ', upload_to='popups/%Y/%m/', help_text='แนะนำขนาด 800x450 พิกเซล (16:9)')

    # Link (Optional)
    link_url = models.CharField('ลิงก์', max_length=500, blank=True, help_text='URL เช่น /education/admission/ หรือ https://example.com')
    link_text = models.CharField('ข้อความลิงก์', max_length=100, blank=True, default='คลิกเพื่อดูรายละเอียด')

    # Display Settings
    is_active = models.BooleanField('เปิดใช้งาน', default=True)
    start_date = models.DateTimeField('วันที่เริ่มแสดง', null=True, blank=True)
    end_date = models.DateTimeField('วันที่สิ้นสุด', null=True, blank=True)

    # Auto-close Settings
    auto_close_delay = models.IntegerField(
        'ปิดอัตโนมัติหลังจาก (วินาที)',
        default=0,
        help_text='0 = ไม่ปิดอัตโนมัติ, ต้องกดปิดเอง'
    )

    # Display Behavior
    SHOW_CHOICES = [
        ('always', 'แสดงทุกครั้ง'),
        ('once_per_session', 'แสดงครั้งเดียวต่อ Session'),
        ('once_per_day', 'แสดงครั้งเดียวต่อวัน'),
        ('once_forever', 'แสดงครั้งเดียวตลอดกาล'),
    ]
    show_frequency = models.CharField(
        'ความถี่การแสดง',
        max_length=20,
        choices=SHOW_CHOICES,
        default='once_per_session'
    )

    # Delay before showing
    show_delay = models.IntegerField(
        'หน่วงเวลาก่อนแสดง (วินาที)',
        default=2,
        help_text='เวลารอก่อนแสดง Popup (0-10 วินาที)'
    )

    # Size
    SIZE_CHOICES = [
        ('small', 'เล็ก (640x360) 16:9'),
        ('medium', 'กลาง (800x450) 16:9'),
        ('large', 'ใหญ่ (1280x720) 16:9'),
    ]
    size = models.CharField(
        'ขนาด',
        max_length=10,
        choices=SIZE_CHOICES,
        default='medium'
    )

    # Analytics
    view_count = models.IntegerField('จำนวนครั้งที่แสดง', default=0, editable=False)
    click_count = models.IntegerField('จำนวนครั้งที่คลิก', default=0, editable=False)

    class Meta:
        verbose_name = 'Popup'
        verbose_name_plural = 'Popup'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def is_visible(self):
        """ตรวจสอบว่า Popup ควรแสดงหรือไม่ตามวันที่"""
        if not self.is_active:
            return False

        from django.utils import timezone
        now = timezone.now()

        if self.start_date and now < self.start_date:
            return False

        if self.end_date and now > self.end_date:
            return False

        return True

    @property
    def click_rate(self):
        """คำนวณ Click Rate (CTR)"""
        if self.view_count == 0:
            return 0
        return round((self.click_count / self.view_count) * 100, 2)

    def increment_view(self):
        """เพิ่มจำนวนครั้งที่แสดง"""
        self.view_count = models.F('view_count') + 1
        self.save(update_fields=['view_count'])
        self.refresh_from_db()

    def increment_click(self):
        """เพิ่มจำนวนครั้งที่คลิก"""
        self.click_count = models.F('click_count') + 1
        self.save(update_fields=['click_count'])
        self.refresh_from_db()
