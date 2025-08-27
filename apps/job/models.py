from django.db import models

from apps.base.choices import UserTypeChoices, SkillChoices, SalaryRange
from apps.users.models import Employer
# Create your models here.

#ONLY EMPLOYERS SHOULD BE ABLE TO POST JOBS
#THEY SHOULD BE ABLE TO CREATE, DELETE AND UPDATE JOB POSTS
class Job(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    jobtype = models.CharField(choices=SkillChoices.choices, blank=False)
    description = models.CharField(max_length=250, blank=False)
    pay = models.PositiveIntegerField(choices=SalaryRange.choices)

