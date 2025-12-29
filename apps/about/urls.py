from django.urls import path
from . import views

app_name = 'about'

urlpatterns = [
    path('', views.AboutIndexView.as_view(), name='index'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('vision-mission/', views.VisionMissionView.as_view(), name='vision_mission'),
    path('dean-message/', views.DeanMessageView.as_view(), name='dean_message'),
    path('executives/', views.ExecutivesView.as_view(), name='executives'),
    path('organization/', views.OrganizationView.as_view(), name='organization'),
    path('departments/', views.DepartmentsView.as_view(), name='departments'),

    # Personnel
    path('personnel/', views.PersonnelIndexView.as_view(), name='personnel'),
    path('personnel/preclinical/', views.PersonnelPreclinicalView.as_view(), name='personnel_preclinical'),
    path('personnel/clinical/', views.PersonnelClinicalView.as_view(), name='personnel_clinical'),
    path('personnel/thai-medicine/', views.PersonnelThaiMedicineView.as_view(), name='personnel_thai_medicine'),
    path('personnel/supporting-staff/', views.PersonnelSupportingStaffView.as_view(), name='personnel_supporting_staff'),

    path('annual-report/', views.AnnualReportView.as_view(), name='annual_report'),
    path('faculty-board/', views.FacultyBoardView.as_view(), name='faculty_board'),
]
