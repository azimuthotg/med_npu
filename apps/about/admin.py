from django.contrib import admin
from .models import Executive, Department, Personnel, Responsibility


@admin.register(Responsibility)
class ResponsibilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    list_editable = ('order', 'is_active')
    ordering = ('order',)


@admin.register(Executive)
class ExecutiveAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position_title', 'position', 'email', 'order', 'is_active')
    list_filter = ('position', 'is_active')
    search_fields = ('first_name', 'last_name', 'position_title')
    list_editable = ('order', 'is_active')
    ordering = ('order',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'department_type', 'head', 'phone', 'order', 'is_active')
    list_filter = ('department_type', 'is_active')
    search_fields = ('name', 'name_en', 'description')
    list_editable = ('order', 'is_active')
    ordering = ('department_type', 'order')


@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'personnel_type', 'position', 'department', 'order', 'is_active')
    list_filter = ('personnel_type', 'is_active', 'department')
    search_fields = ('first_name', 'last_name', 'position', 'specialization')
    list_editable = ('order', 'is_active')
    ordering = ('personnel_type', 'order')
    filter_horizontal = ('responsibilities',)
