from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, 
    SkillModel, 
    ProjectModel, 
    ExperienceModel, 
    EducationModel, 
    ContactMessage
)

# Register CustomUser with UserAdmin so dashboard password hashing works safely
admin.site.register(CustomUser, UserAdmin)

# Register all other models in your favorite simple array format
admin.site.register([
    SkillModel,
    ProjectModel,
    ExperienceModel,
    EducationModel,
    ContactMessage
])