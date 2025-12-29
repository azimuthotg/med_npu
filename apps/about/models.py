from django.db import models
from apps.core.models import TimeStampedModel


class Executive(TimeStampedModel):
    """ผู้บริหาร"""
    POSITION_CHOICES = [
        ('dean', 'คณบดี'),
        ('vice_dean', 'รองคณบดี'),
        ('assistant_dean', 'ผู้ช่วยคณบดี'),
        ('head', 'หัวหน้าภาควิชา'),
        ('other', 'อื่นๆ'),
    ]
    
    title = models.CharField('คำนำหน้า', max_length=50, 
        help_text='เช่น ศ.นพ., รศ.ดร.นพ.')
    first_name = models.CharField('ชื่อ', max_length=100)
    last_name = models.CharField('นามสกุล', max_length=100)
    position = models.CharField('ประเภทตำแหน่ง', max_length=20, choices=POSITION_CHOICES)
    position_title = models.CharField('ชื่อตำแหน่ง', max_length=200)
    photo = models.ImageField('รูปภาพ', upload_to='executives/', blank=True, null=True)
    email = models.EmailField('อีเมล', blank=True)
    phone = models.CharField('โทรศัพท์', max_length=50, blank=True)
    order = models.PositiveIntegerField('ลำดับการแสดง', default=0)
    is_active = models.BooleanField('แสดง', default=True)
    
    class Meta:
        verbose_name = 'ผู้บริหาร'
        verbose_name_plural = 'ผู้บริหาร'
        ordering = ['order', 'position']
    
    def __str__(self):
        return f"{self.title}{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.title}{self.first_name} {self.last_name}"


class Department(TimeStampedModel):
    """ภาควิชา/หน่วยงาน"""
    name = models.CharField('ชื่อภาควิชา', max_length=200)
    name_en = models.CharField('ชื่อภาษาอังกฤษ', max_length=200, blank=True)
    description = models.TextField('รายละเอียด', blank=True)
    head = models.ForeignKey(
        Executive, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='หัวหน้าภาควิชา'
    )
    phone = models.CharField('โทรศัพท์', max_length=50, blank=True)
    email = models.EmailField('อีเมล', blank=True)
    order = models.PositiveIntegerField('ลำดับการแสดง', default=0)
    is_active = models.BooleanField('แสดง', default=True)
    
    class Meta:
        verbose_name = 'ภาควิชา'
        verbose_name_plural = 'ภาควิชา/หน่วยงาน'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
