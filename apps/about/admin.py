from django.contrib import admin
from .models import Executive, Department


@admin.register(Executive)
class ExecutiveAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position_title', 'position', 'email', 'order', 'is_active')
    list_filter = ('position', 'is_active')
    search_fields = ('first_name', 'last_name', 'position_title')
    list_editable = ('order', 'is_active')
    ordering = ('order',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head', 'phone', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'name_en')
    list_editable = ('order', 'is_active')
    ordering = ('order',)
