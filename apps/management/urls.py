"""
URL configuration for management app
"""
from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    # Authentication
    path('login/', views.ManagementLoginView.as_view(), name='login'),
    path('logout/', views.ManagementLogoutView.as_view(), name='logout'),

    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),

    # News Management
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/create/', views.NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', views.NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),

    # Category Management
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),

    # Gallery Management
    path('galleries/', views.GalleryListView.as_view(), name='gallery_list'),
    path('galleries/create/', views.GalleryCreateView.as_view(), name='gallery_create'),
    path('galleries/<int:pk>/edit/', views.GalleryUpdateView.as_view(), name='gallery_edit'),
    path('galleries/<int:pk>/delete/', views.GalleryDeleteView.as_view(), name='gallery_delete'),
    path('galleries/<int:pk>/images/', views.GalleryImageManageView.as_view(), name='gallery_images'),
    path('galleries/<int:gallery_pk>/images/add/', views.GalleryImageCreateView.as_view(), name='gallery_image_add'),
    path('galleries/<int:gallery_pk>/images/bulk-upload/', views.GalleryBulkUploadView.as_view(), name='gallery_bulk_upload'),
    path('galleries/images/<int:pk>/edit/', views.GalleryImageUpdateView.as_view(), name='gallery_image_edit'),
    path('galleries/images/<int:pk>/delete/', views.GalleryImageDeleteView.as_view(), name='gallery_image_delete'),

    # Executive Management
    path('executives/', views.ExecutiveListView.as_view(), name='executive_list'),
    path('executives/create/', views.ExecutiveCreateView.as_view(), name='executive_create'),
    path('executives/<int:pk>/edit/', views.ExecutiveUpdateView.as_view(), name='executive_edit'),
    path('executives/<int:pk>/delete/', views.ExecutiveDeleteView.as_view(), name='executive_delete'),

    # Department Management
    path('departments/', views.DepartmentListView.as_view(), name='department_list'),
    path('departments/create/', views.DepartmentCreateView.as_view(), name='department_create'),
    path('departments/<int:pk>/edit/', views.DepartmentUpdateView.as_view(), name='department_edit'),
    path('departments/<int:pk>/delete/', views.DepartmentDeleteView.as_view(), name='department_delete'),

    # Program Management
    path('programs/', views.ProgramListView.as_view(), name='program_list'),
    path('programs/create/', views.ProgramCreateView.as_view(), name='program_create'),
    path('programs/<int:pk>/edit/', views.ProgramUpdateView.as_view(), name='program_edit'),
    path('programs/<int:pk>/delete/', views.ProgramDeleteView.as_view(), name='program_delete'),

    # Admission Management
    path('admissions/', views.AdmissionListView.as_view(), name='admission_list'),
    path('admissions/create/', views.AdmissionCreateView.as_view(), name='admission_create'),
    path('admissions/<int:pk>/edit/', views.AdmissionUpdateView.as_view(), name='admission_edit'),
    path('admissions/<int:pk>/delete/', views.AdmissionDeleteView.as_view(), name='admission_delete'),

    # Banner Management
    path('banners/', views.BannerListView.as_view(), name='banner_list'),
    path('banners/create/', views.BannerCreateView.as_view(), name='banner_create'),
    path('banners/<int:pk>/edit/', views.BannerUpdateView.as_view(), name='banner_edit'),
    path('banners/<int:pk>/delete/', views.BannerDeleteView.as_view(), name='banner_delete'),

    # Popup Management
    path('popups/', views.PopupListView.as_view(), name='popup_list'),
    path('popups/create/', views.PopupCreateView.as_view(), name='popup_create'),
    path('popups/<int:pk>/edit/', views.PopupUpdateView.as_view(), name='popup_edit'),
    path('popups/<int:pk>/delete/', views.PopupDeleteView.as_view(), name='popup_delete'),

    # Site Settings
    path('settings/', views.SiteSettingsView.as_view(), name='settings'),
]
