from django.contrib import admin
from .models import Program, Admission


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'degree', 'level', 'duration', 'is_active', 'order')
    list_filter = ('level', 'is_active')
    search_fields = ('name', 'name_en')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order', 'is_active')
    ordering = ('order',)


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'program', 
        'academic_year', 
        'round_name',
        'start_date', 
        'end_date', 
        'quota',
        'is_active'
    )
    list_filter = ('academic_year', 'program', 'is_active')
    search_fields = ('title',)
    date_hierarchy = 'start_date'
    ordering = ('-academic_year', '-start_date')
