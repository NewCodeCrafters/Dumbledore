from django.db import models

class UserTypeChoices(models.TextChoices):
    USER = "user", "User"
    EMPLOYER = "employer", "Employer"
    JOBSEEKER= "jobseeker", "Jobseeker"
    ADMIN = "admin", "Admin"


class StatusChoices(models.TextChoices):
    DEFAULT = "default", "Default"
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    PENDING = "pending", "Pending"
    SUSPENDED = "suspended", "Suspended"
    DELETED = "deleted", "Deleted"
    BLOCKED = "blocked", "Blocked"


class SkillChoices(models.TextChoices):
    WEB_DEVELOPMENT = 'Web Development', 'Web Development'
    MOBILE_DEVELOPMENT = 'Mobile Development', 'Mobile Development'
    DATA_ANALYSIS = 'Data Analysis', 'Data Analysis'
    GRAPHIC_DESIGN = 'Graphic Design', 'Graphic Design'
    CONTENT_WRITING = 'Content Writing', 'Content Writing'
    DIGITAL_MARKETING = 'Digital Marketing', 'Digital Marketing'
    SEO = 'SEO', 'SEO'
    OTHER = 'Other', 'Other'
    HEALTHCARE = 'healthcare', 'Healthcare'



class AvailabilityChoices(models.TextChoices):
    FULL_TIME = 'Full Time', 'Full Time'
    PART_TIME = 'Part Time', 'Part Time'
    FREELANCE = 'Freelance', 'Freelance'
    ON_CALL = 'On Call', 'On Call'
    NOT_AVAILABLE = 'Not Available', 'Not Available'


class ExperienceLevelChoices(models.TextChoices):
    NOVICE = 'novice', 'Novice'
    PROFESSIONAL = 'professional', 'Professional'
    SENIOR_LEVEL = 'senior_level', 'Senior Level'
    EXPERT = 'expert', 'Expert'


class TimeZoneChoices(models.TextChoices):
    UTC = 'UTC', 'UTC'
    EST = 'EST', 'Eastern Standard Time'
    PST = 'PST', 'Pacific Standard Time'
    CST = 'CST', 'Central Standard Time'
    GMT = 'GMT', 'Greenwich Mean Time'
    IST = 'IST', 'Indian Standard Time'
    CET = 'CET', 'Central European Time'
    JST = 'JST', 'Japan Standard Time'

class OtherSkill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class SalaryRange(models.TextChoices):
    LOW = "5,000", "10,000"
    BELOW_AVERAGE = "10,000", "20,000"
    AVERAGE = "20,000", "40,000"
    ABOVE_AVERAGE = "40,000", "60,000"
    HIGH = "60,000", "100,000"