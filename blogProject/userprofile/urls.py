from django.urls import path
from . import views

app_name = 'userprofile'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('profile/<int:id>/', views.profile_view, name='profile'),
    path('edit/<int:id>/', views.profile_edit, name='edit'),
    path('contact', views.contact, name='contact'),
    path('resume/', views.show_resume, name='resume'),
    path('editResumePersonalInfo/', views.resumePersonalInfo_edit, name='editResumePersonalInfo'),
    path('showResumeEducation/', views.showResumeEducation, name='showResumeEducation'),
    path('editResumeEducation/<int:id>/', views.resumeEducation_edit, name='editResumeEducation'),
    path('addResumeEducation/', views.resumeEducation_add, name='resumeEducation_add'),
    path('deleteResumeEducation/<int:id>', views.resumeEducation_delete, name='resumeEducation_delete'),
    path('showResumeJob/', views.showResumeJob, name='showResumeJob'),
    path('editResumeJob/<int:id>/', views.resumeJob_edit, name='editResumeJob'),
    path('addResumeJob/', views.resumeJob_add, name='resumeJob_add'),
    path('deleteResumeJob/<int:id>', views.resumeJob_delete, name='resumeJob_delete'),
    path('showResumeResearch/', views.showResumeResearch, name='showResumeResearch'),
    path('editResumeResearch/<int:id>/', views.resumeReseach_edit, name='editResumeResearch'),
    path('addResumeResearch/', views.resumeResearch_add, name='resumeResearch_add'),
    path('deleteResumeResearch/<int:id>', views.resumeResearch_delete, name='resumeResearch_delete'),
]
