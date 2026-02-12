from rest_framework import serializers
from .models import Job, Category, Application
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class JobSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)  # do NOT send in POST

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'location', 'job_type', 'created_by', 'category', 'created_at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ApplicationSerializer(serializers.ModelSerializer):
    applicant = UserSerializer(read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'applicant', 'job', 'resume', 'cover_letter', 'applied_at']

