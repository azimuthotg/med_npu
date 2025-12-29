from django.urls import path
from . import views

app_name = 'education'

urlpatterns = [
    path('', views.EducationIndexView.as_view(), name='index'),
    path('programs/', views.ProgramListView.as_view(), name='program_list'),
    path('programs/<slug:slug>/', views.ProgramDetailView.as_view(), name='program_detail'),
    path('admissions/', views.AdmissionListView.as_view(), name='admission_list'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('foundation/', views.FoundationView.as_view(), name='foundation'),
    path('scholarship/', views.ScholarshipView.as_view(), name='scholarship'),
]
