from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import AuthenticationForm
from .forms import (
    ContactForm,
    EducationForm,
    ExperienceForm,
    ProjectForm,
    SkillForm,
    UserProfileForm,
    UserRegisterForm,
)
from .models import (
    ContactMessage,
    CustomUser,
    EducationModel,
    ExperienceModel,
    ProjectModel,
    SkillModel,
)


# ==================== PUBLIC VIEWS ====================


def get_portfolio_user(request):
    """Return the portfolio user (owner) for public pages.

    Returns the first user (site owner) for all visitors.
    """
    return CustomUser.objects.order_by('id').first()


def home(request):
    """Main portfolio landing page with all sections."""
    profile_user = get_portfolio_user(request)
    
    skills = SkillModel.objects.filter(user=profile_user) if profile_user else []
    featured_skills = skills[:3]
    featured_projects = ProjectModel.objects.filter(user=profile_user)[:4] if profile_user else []
    featured_experience = ExperienceModel.objects.filter(user=profile_user)[:3] if profile_user else []
    education = EducationModel.objects.filter(user=profile_user) if profile_user else []

    return render(request, 'home.html', {
        'profile': profile_user,
        'skills': skills,
        'projects': featured_projects,
        'experiences': featured_experience,
        'education': education,
        'featured_skills': featured_skills,
    })


def about_view(request):
    """About page with full bio and details."""
    profile_user = get_portfolio_user(request)
    experiences = ExperienceModel.objects.filter(user=profile_user) if profile_user else []
    education = EducationModel.objects.filter(user=profile_user) if profile_user else []

    return render(request, 'about.html', {
        'profile': profile_user,
        'experiences': experiences,
        'education': education,
    })


def skills_view(request):
    """Skills showcase page."""
    profile_user = get_portfolio_user(request)
    skills = SkillModel.objects.filter(user=profile_user) if profile_user else []

    return render(request, 'skills.html', {
        'profile': profile_user,
        'skills': skills,
    })


def projects_view(request):
    """Projects listing page."""
    profile_user = get_portfolio_user(request)
    projects = ProjectModel.objects.filter(user=profile_user) if profile_user else []

    return render(request, 'projects.html', {
        'profile': profile_user,
        'projects': projects,
    })


def project_detail_view(request, pk):
    """Project detail page."""
    project = get_object_or_404(ProjectModel, pk=pk)

    return render(request, 'project_detail.html', {
        'project': project,
    })


def resume_view(request):
    """Resume/CV page."""
    profile_user = get_portfolio_user(request)
    skills = SkillModel.objects.filter(user=profile_user) if profile_user else []
    projects = ProjectModel.objects.filter(user=profile_user) if profile_user else []
    experiences = ExperienceModel.objects.filter(user=profile_user) if profile_user else []
    education = EducationModel.objects.filter(user=profile_user) if profile_user else []

    return render(request, 'resume.html', {
        'profile': profile_user,
        'skills': skills,
        'projects': projects,
        'experiences': experiences,
        'education': education,
    })


def contact_view(request):
    """Contact form page."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('home')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {
        'form': form,
    })


# ==================== AUTHENTICATION VIEWS ====================

def register_view(request):
    """User registration page."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully.')
            return redirect('dashboard')
    else:
        form = UserRegisterForm()

    return render(request, 'master/base-form.html', {
        'form_name': 'Register',
        'form_data': form,
        'form_btn': 'Create Account',
    })


def login_view(request):
    """User login page."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm(request)

    return render(request, 'master/base-form.html', {
        'form_name': 'Login',
        'form_data': form,
        'form_btn': 'Login',
    })


# ==================== ADMIN DASHBOARD VIEWS ====================

@login_required
def dashboard(request):
    user = request.user

    skills = SkillModel.objects.filter(user=user)
    projects = ProjectModel.objects.filter(user=user)
    experiences = ExperienceModel.objects.filter(user=user)
    education = EducationModel.objects.filter(user=user)

    # ADJUSTED: Points to 'dashbord.html' at root level based on your directory spelling
    return render(request, 'dashbord.html', {
        'skills': skills,
        'projects': projects,
        'experiences': experiences,
        'education': education,
        'skills_count': skills.count(),
        'projects_count': projects.count(),
        'experiences_count': experiences.count(),
        'education_count': education.count(),
    })


@login_required
def profile_edit(request):
    """Edit admin profile."""
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'master/base-form.html', {
        'form_name': 'Edit Profile',
        'form_data': form,
        'form_btn': 'Save Changes',
    })


# ==================== SKILL MANAGEMENT ====================

@login_required
def skill_list(request):
    skills = SkillModel.objects.filter(user=request.user)
    # ADJUSTED: Points to root templates directory as seen in tree layout
    return render(request, 'skills.html', {'skills': skills})


@login_required
def skill_create(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            messages.success(request, 'Skill added successfully.')
            return redirect('dashboard')  # Redirect straight to dashboard for clean UX
    else:
        form = SkillForm()

    return render(request, 'master/base-form.html', {
        'form_name': 'Add Skill',
        'form_data': form,
        'form_btn': 'Add Skill',
    })


@login_required
def skill_edit(request, pk):
    skill = get_object_or_404(SkillModel, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated successfully.')
            return redirect('dashboard')
    else:
        form = SkillForm(instance=skill)

    return render(request, 'master/base-form.html', {
        'form_name': 'Edit Skill',
        'form_data': form,
        'form_btn': 'Save Skill',
    })


@login_required
def skill_delete(request, pk):
    skill = get_object_or_404(SkillModel, pk=pk, user=request.user)
    skill.delete()
    messages.success(request, 'Skill deleted.')
    return redirect('dashboard')


# ==================== PROJECT MANAGEMENT ====================

@login_required
def project_list(request):
    projects = ProjectModel.objects.filter(user=request.user)
    # ADJUSTED: Points to root templates directory
    return render(request, 'projects.html', {'projects': projects})


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            messages.success(request, 'Project added successfully.')
            return redirect('dashboard')
    else:
        form = ProjectForm()

    return render(request, 'master/base-form.html', {
        'form_name': 'Add Project',
        'form_data': form,
        'form_btn': 'Add Project',
    })


@login_required
def project_edit(request, pk):
    project = get_object_or_404(ProjectModel, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully.')
            return redirect('dashboard')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'master/base-form.html', {
        'form_name': 'Edit Project',
        'form_data': form,
        'form_btn': 'Save Project',
    })


@login_required
def project_delete(request, pk):
    project = get_object_or_404(ProjectModel, pk=pk, user=request.user)
    project.delete()
    messages.success(request, 'Project deleted.')
    return redirect('dashboard')


# ==================== EXPERIENCE MANAGEMENT ====================

@login_required
def experience_list(request):
    experiences = ExperienceModel.objects.filter(user=request.user)
    # ADJUSTED: Redirects or defaults back to dashboard info blocks
    return redirect('dashboard')


@login_required
def experience_create(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user
            experience.save()
            messages.success(request, 'Experience added successfully.')
            return redirect('dashboard')
    else:
        form = ExperienceForm()

    return render(request, 'master/base-form.html', {
        'form_name': 'Add Experience',
        'form_data': form,
        'form_btn': 'Add Experience',
    })


@login_required
def experience_edit(request, pk):
    experience = get_object_or_404(ExperienceModel, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            messages.success(request, 'Experience updated successfully.')
            return redirect('dashboard')
    else:
        form = ExperienceForm(instance=experience)

    return render(request, 'master/base-form.html', {
        'form_name': 'Edit Experience',
        'form_data': form,
        'form_btn': 'Save Experience',
    })


@login_required
def experience_delete(request, pk):
    experience = get_object_or_404(ExperienceModel, pk=pk, user=request.user)
    experience.delete()
    messages.success(request, 'Experience deleted.')
    return redirect('dashboard')


# ==================== EDUCATION MANAGEMENT ====================

@login_required
def education_list(request):
    return redirect('dashboard')


@login_required
def education_create(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education_entry = form.save(commit=False)
            education_entry.user = request.user
            education_entry.save()
            messages.success(request, 'Education added successfully.')
            return redirect('dashboard')
    else:
        form = EducationForm()

    return render(request, 'master/base-form.html', {
        'form_name': 'Add Education',
        'form_data': form,
        'form_btn': 'Add Education',
    })


@login_required
def education_edit(request, pk):
    education_entry = get_object_or_404(EducationModel, pk=pk, user=request.user)
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education_entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Education updated successfully.')
            return redirect('dashboard')
    else:
        form = EducationForm(instance=education_entry)

    return render(request, 'master/base-form.html', {
        'form_name': 'Edit Education',
        'form_data': form,
        'form_btn': 'Save Education',
    })


@login_required
def education_delete(request, pk):
    education_entry = get_object_or_404(EducationModel, pk=pk, user=request.user)
    education_entry.delete()
    messages.success(request, 'Education deleted.')
    return redirect('dashboard')


# ==================== MESSAGES MANAGEMENT ====================

@login_required
def messages_view(request):
    contact_messages = ContactMessage.objects.all()
    return render(request, 'messages.html', {
        'messages_list': contact_messages,
    })


@login_required
def message_delete(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    message.delete()
    messages.success(request, 'Message deleted.')
    return redirect('messages_view')