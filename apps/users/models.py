from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from apps.base.choices import UserTypeChoices , SkillChoices, AvailabilityChoices, OtherSkill, TimeZoneChoices, ExperienceLevelChoices, SalaryRange, StatusChoices
from apps.base.models import BaseModel

from .managers import UserManager

class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    user_type = models.CharField(max_length=20, choices=UserTypeChoices.choices, default=UserTypeChoices.USER)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at  = models.DateTimeField(blank=True, null=True)
    is_employer = models.BooleanField(default=False)
    is_seeking_job = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    otp_verified = models.BooleanField(default=False)
    cv = models.FileField(upload_to='cv/', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name",]

    objects = UserManager() 
    
    def __str__(self):
        return self.first_name


    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name    

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    company_description = models.TextField()
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name
    

class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    availability_status = models.CharField(AvailabilityChoices.choices, null=True, default=AvailabilityChoices.NOT_AVAILABLE)
    expertise = models.CharField(SkillChoices.choices)
    



    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    # location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name}'s Profile"