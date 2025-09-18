from rest_framework import serializers # type: ignore

from .models import Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = (
            "employer", "description", "jobtype", "pay", "created_at"
        )