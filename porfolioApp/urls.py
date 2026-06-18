from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Public Client View Paths
    path('', views.home, name='home'),
    path('about/', views.about_view, name='about'),
    path('skills/', views.skills_view, name='skills'),
    path('projects/', views.projects_view, name='projects'),
    path('project/<int:pk>/', views.project_detail_view, name='project_detail'),
    path('resume/', views.resume_view, name='resume'),
    path('contact/', views.contact_view, name='contact'),
    
    # User Session & Registration Routing System
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    # swap auth_views.LogoutVew out for a basic function view to avoid 405 Method errors.
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # Internal Portfolio Admin Control Panel Options
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    
    # Skill Item Management Routines
    path('skill-list/', views.skill_list, name='skill_list'),
    path('skill/add/', views.skill_create, name='skill_create'),
    path('skill/<int:pk>/edit/', views.skill_edit, name='skill_edit'),
    path('skill/<int:pk>/delete/', views.skill_delete, name='skill_delete'),
    
    # Showcase Project Management Routines
    path('projects-manage/', views.project_list, name='project_list'),
    path('project/add/', views.project_create, name='project_create'),
    path('project/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('project/<int:pk>/delete/', views.project_delete, name='project_delete'),
    
    # Corporate Experience Management Routines
    path('experience-manage/', views.experience_list, name='experience_list'),
    path('experience/add/', views.experience_create, name='experience_create'),
    path('experience/<int:pk>/edit/', views.experience_edit, name='experience_edit'),
    path('experience/<int:pk>/delete/', views.experience_delete, name='experience_delete'),
    
    # Academic Education Profile Routines
    path('education-manage/', views.education_list, name='education_list'),
    path('education/add/', views.education_create, name='education_create'),
    path('education/<int:pk>/edit/', views.education_edit, name='education_edit'),
    path('education/<int:pk>/delete/', views.education_delete, name='education_delete'),
    
    # Contact Inquiry Message System Options
    path('messages/', views.messages_view, name='messages_view'),
    path('message/<int:pk>/delete/', views.message_delete, name='message_delete'),
]