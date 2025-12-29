from django.db import models
from django.urls import reverse
from apps.core.models import TimeStampedModel


class Program(TimeStampedModel):
    """หลักสูตร"""
    LEVEL_CHOICES = [
        ('bachelor', 'ปริญญาตรี'),
        ('master', 'ปริญญาโท'),
        ('doctoral', 'ปริญญาเอก'),
        ('diploma', 'ประกาศนียบัตร'),
    ]
    
    name = models.CharField('ชื่อหลักสูตร', max_length=300)
    name_en = models.CharField('ชื่อภาษาอังกฤษ', max_length=300, blank=True)
    slug = models.SlugField('Slug', unique=True, allow_unicode=True)
    level = models.CharField('ระดับ', max_length=20, choices=LEVEL_CHOICES)
    degree = models.CharField('ชื่อปริญญา', max_length=100, 
        help_text='เช่น พ.บ., วท.ม.')
    degree_en = models.CharField('ชื่อปริญญาภาษาอังกฤษ', max_length=100, blank=True,
        help_text='เช่น M.D., M.Sc.')
    duration = models.CharField('ระยะเวลาเรียน', max_length=50, 
        help_text='เช่น 6 ปี')
    description = models.TextField('รายละเอียด', blank=True)
    curriculum_file = models.FileField('ไฟล์หลักสูตร (PDF)', 
        upload_to='education/programs/', blank=True, null=True)
    image = models.ImageField('รูปภาพ', upload_to='education/programs/', 
        blank=True, null=True)
    
    is_active = models.BooleanField('เปิดสอน', default=True)
    order = models.PositiveIntegerField('ลำดับการแสดง', default=0)
    
    class Meta:
        verbose_name = 'หลักสูตร'
        verbose_name_plural = 'หลักสูตร'
        ordering = ['order', 'level', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.degree})"
    
    def get_absolute_url(self):
        return reverse('education:program_detail', kwargs={'slug': self.slug})


class Admission(TimeStampedModel):
    """ประกาศรับสมัคร"""
    title = models.CharField('หัวข้อ', max_length=300)
    program = models.ForeignKey(
        Program, 
        on_delete=models.CASCADE,
        verbose_name='หลักสูตร'
    )
    academic_year = models.CharField('ปีการศึกษา', max_length=10, 
        help_text='เช่น 2568')
    round_name = models.CharField('รอบการรับสมัคร', max_length=100,
        help_text='เช่น Portfolio, Quota, Admission')
    
    start_date = models.DateField('วันเริ่มรับสมัคร')
    end_date = models.DateField('วันสิ้นสุดรับสมัคร')
    
    quota = models.PositiveIntegerField('จำนวนรับ', default=0)
    description = models.TextField('รายละเอียด', blank=True)
    requirements = models.TextField('คุณสมบัติผู้สมัคร', blank=True)
    
    announcement_file = models.FileField('ไฟล์ประกาศ', 
        upload_to='education/admissions/', blank=True, null=True)
    apply_url = models.URLField('ลิงก์สมัคร', blank=True)
    
    is_active = models.BooleanField('เปิดรับสมัคร', default=True)
    
    class Meta:
        verbose_name = 'ประกาศรับสมัคร'
        verbose_name_plural = 'ประกาศรับสมัคร'
        ordering = ['-academic_year', '-start_date']
    
    def __str__(self):
        return f"{self.title} ({self.academic_year})"
    
    @property
    def is_open(self):
        from django.utils import timezone
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date and self.is_active
