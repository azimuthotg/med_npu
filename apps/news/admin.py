from django.contrib import admin
from django.utils.html import format_html
from .models import Category, News, NewsAttachment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


class NewsAttachmentInline(admin.TabularInline):
    model = NewsAttachment
    extra = 1


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'category', 
        'is_published', 
        'is_featured',
        'published_at', 
        'view_count'
    )
    list_filter = ('is_published', 'is_featured', 'category', 'published_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering = ('-published_at',)
    
    fieldsets = (
        ('ข้อมูลหลัก', {
            'fields': ('title', 'slug', 'category', 'excerpt', 'content')
        }),
        ('รูปภาพ', {
            'fields': ('featured_image',)
        }),
        ('การเผยแพร่', {
            'fields': ('is_published', 'is_featured', 'published_at')
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [NewsAttachmentInline]
    
    def save_model(self, request, obj, form, change):
        # Auto-fill excerpt from content if empty
        if not obj.excerpt and obj.content:
            obj.excerpt = obj.content[:200] + '...' if len(obj.content) > 200 else obj.content
        super().save_model(request, obj, form, change)
