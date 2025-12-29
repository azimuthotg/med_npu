from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('download/', views.DownloadView.as_view(), name='download'),
    path('search/', views.SearchView.as_view(), name='search'),

    # Research & Academic Services
    path('research-services/', views.ResearchServicesView.as_view(), name='research_services'),
    path('research-services/research-centers/', views.ResearchCentersView.as_view(), name='research_centers'),
    path('research-services/research-projects/', views.ResearchProjectsView.as_view(), name='research_projects'),
    path('research-services/publications/', views.PublicationsView.as_view(), name='publications'),
    path('research-services/research-ethics/', views.ResearchEthicsView.as_view(), name='research_ethics'),
    path('research-services/community-services/', views.CommunityServicesView.as_view(), name='community_services'),
    path('research-services/training-courses/', views.TrainingCoursesView.as_view(), name='training_courses'),
    path('research-services/collaboration/', views.CollaborationView.as_view(), name='collaboration'),

    # Quality Assurance
    path('quality-assurance/wfme/', views.QAWFMEView.as_view(), name='qa_wfme'),
    path('quality-assurance/edpex/', views.QAEdPExView.as_view(), name='qa_edpex'),
    path('quality-assurance/aunqa/', views.QAAUNQAView.as_view(), name='qa_aunqa'),
    path('quality-assurance/npuqa/', views.QANPUQAView.as_view(), name='qa_npuqa'),
]
