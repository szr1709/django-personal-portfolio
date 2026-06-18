from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, SkillModel, ProjectModel, ExperienceModel, EducationModel, ContactMessage

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        # password1 and password2 removed to avoid server crashes
        fields = ['username', 'email']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'headline', 'bio', 'location', 'phone', 'profile_picture', 'cv_summary']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'cv_summary': forms.Textarea(attrs={'rows': 3}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = SkillModel
        fields = ['name', 'level']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = ProjectModel
        fields = '__all__'
        exclude = ['user']


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = ExperienceModel
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'})
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = EducationModel
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'})
        }