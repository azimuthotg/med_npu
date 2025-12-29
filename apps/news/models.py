from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from apps.core.models import TimeStampedModel


class Category(models.Model):
    """หมวดหมู่ข่าว"""
    name = models.CharField('ชื่อหมวดหมู่', max_length=100)
    slug = models.SlugField('Slug', max_length=200, unique=True, allow_unicode=True, blank=True)
    color = models.CharField('สี', max_length=20, default='primary',
        help_text='primary, blue, green, purple, orange')
    
    class Meta:
        verbose_name = 'หมวดหมู่ข่าว'
        verbose_name_plural = 'หมวดหมู่ข่าว'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class News(TimeStampedModel):
    """ข่าวประชาสัมพันธ์"""
    title = models.CharField('หัวข้อข่าว', max_length=300)
    slug = models.SlugField('Slug', max_length=200, unique=True, allow_unicode=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='หมวดหมู่'
    )
    gallery = models.ForeignKey(
        'gallery.Gallery',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='news_items',
        verbose_name='อัลบั้มภาพกิจกรรม',
        help_text='เลือกอัลบั้มภาพที่เกี่ยวข้องกับข่าวนี้'
    )
    excerpt = models.TextField('เนื้อหาย่อ', max_length=500, blank=True)
    content = models.TextField('เนื้อหา')
    featured_image = models.ImageField(
        'รูปภาพประกอบ', 
        upload_to='news/%Y/%m/', 
        blank=True, 
        null=True
    )
    
    # Publishing
    is_published = models.BooleanField('เผยแพร่', default=True)
    is_featured = models.BooleanField('ข่าวเด่น', default=False)
    published_at = models.DateTimeField('วันที่เผยแพร่', default=timezone.now)
    
    # SEO
    meta_description = models.TextField('Meta Description', blank=True, max_length=160)
    
    # Stats
    view_count = models.PositiveIntegerField('จำนวนเข้าชม', default=0)
    
    class Meta:
        verbose_name = 'ข่าว'
        verbose_name_plural = 'ข่าวประชาสัมพันธ์'
        ordering = ['-published_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # จำกัดความยาว slug ไว้ที่ 180 ตัวอักษร (เหลือที่ว่างสำหรับ -counter)
            base_slug = slugify(self.title, allow_unicode=True)[:180]
            slug = base_slug
            counter = 1
            while News.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'slug': self.slug})
    
    def increment_view(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])


class NewsAttachment(models.Model):
    """ไฟล์แนบข่าว"""
    news = models.ForeignKey(
        News, 
        on_delete=models.CASCADE, 
        related_name='attachments',
        verbose_name='ข่าว'
    )
    file = models.FileField('ไฟล์', upload_to='news/attachments/%Y/%m/')
    name = models.CharField('ชื่อไฟล์', max_length=200, blank=True)
    
    class Meta:
        verbose_name = 'ไฟล์แนบ'
        verbose_name_plural = 'ไฟล์แนบ'
    
    def __str__(self):
        return self.name or self.file.name
