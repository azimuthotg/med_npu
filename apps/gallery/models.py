from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from apps.core.models import TimeStampedModel
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class Gallery(TimeStampedModel):
    """อัลบั้มภาพกิจกรรม"""
    title = models.CharField('ชื่ออัลบั้ม', max_length=200)
    slug = models.SlugField('Slug', max_length=200, unique=True, allow_unicode=True, blank=True)
    description = models.TextField('คำอธิบาย', blank=True)
    cover_image = models.ImageField(
        'รูปปก',
        upload_to='gallery/covers/%Y/%m/',
        blank=True,
        null=True,
        help_text='รูปปกของอัลบั้ม (แนะนำขนาด 1200x800 px)'
    )
    event_date = models.DateField('วันที่จัดกิจกรรม', null=True, blank=True)
    is_published = models.BooleanField('เผยแพร่', default=True)
    order = models.IntegerField('ลำดับการแสดงผล', default=0)

    class Meta:
        verbose_name = 'อัลบั้มภาพ'
        verbose_name_plural = 'อัลบั้มภาพกิจกรรม'
        ordering = ['-order', '-event_date', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)[:180]
            slug = base_slug
            counter = 1
            while Gallery.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('gallery:detail', kwargs={'slug': self.slug})

    @property
    def image_count(self):
        """จำนวนรูปภาพในอัลบั้ม"""
        return self.images.count()


class GalleryImage(models.Model):
    """รูปภาพในอัลบั้ม"""
    gallery = models.ForeignKey(
        Gallery,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='อัลบั้ม'
    )
    image = models.ImageField('รูปภาพต้นฉบับ', upload_to='gallery/images/%Y/%m/')
    thumbnail = models.ImageField('รูปย่อ', upload_to='gallery/thumbnails/%Y/%m/', blank=True)
    medium = models.ImageField('รูปขนาดกลาง', upload_to='gallery/medium/%Y/%m/', blank=True)
    caption = models.CharField('คำบรรยาย', max_length=500, blank=True)
    order = models.IntegerField('ลำดับ', default=0)

    class Meta:
        verbose_name = 'รูปภาพ'
        verbose_name_plural = 'รูปภาพในอัลบั้ม'
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.gallery.title} - รูปที่ {self.order}"

    def save(self, *args, **kwargs):
        # สร้าง thumbnail และ medium size เมื่ออัปโหลดรูปใหม่
        if self.image and not self.thumbnail:
            self._create_resized_images()
        super().save(*args, **kwargs)

    def _create_resized_images(self):
        """สร้างรูปย่อและรูปขนาดกลาง"""
        img = Image.open(self.image)

        # Convert RGBA to RGB if needed
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background

        # สร้าง Thumbnail (400x400)
        self.thumbnail = self._resize_image(img, (400, 400), 'thumb')

        # สร้าง Medium (1200x800)
        self.medium = self._resize_image(img, (1200, 800), 'medium')

    def _resize_image(self, img, size, prefix):
        """Resize รูปภาพและ return InMemoryUploadedFile"""
        img_copy = img.copy()
        img_copy.thumbnail(size, Image.Resampling.LANCZOS)

        # Save to BytesIO
        output = BytesIO()
        img_copy.save(output, format='JPEG', quality=85, optimize=True)
        output.seek(0)

        # Create filename
        original_name = self.image.name.split('/')[-1]
        name_parts = original_name.rsplit('.', 1)
        new_name = f"{prefix}_{name_parts[0]}.jpg"

        # Return InMemoryUploadedFile
        return InMemoryUploadedFile(
            output,
            'ImageField',
            new_name,
            'image/jpeg',
            sys.getsizeof(output),
            None
        )
