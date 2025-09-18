from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .serializers import JobSerializer
from .models import Job

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer