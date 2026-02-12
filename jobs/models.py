from django.db import models
from django.contrib.auth.models import User

# ---------------------------
# CATEGORY MODEL
# ---------------------------
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# ---------------------------
# JOB MODEL
# ---------------------------
class Job(models.Model):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"
    INTERNSHIP = "internship"
    CONTRACT = "contract"

    JOB_TYPE_CHOICES = [
        (FULL_TIME, "Full-time"),
        (PART_TIME, "Part-time"),
        (INTERNSHIP, "Internship"),
        (CONTRACT, "Contract"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="jobs")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.location}"


# ---------------------------
# APPLICATION MODEL
# ---------------------------
class Application(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("applicant", "job")

    def __str__(self):
        return f"{self.applicant.username} -> {self.job.title}"


# ---------------------------
# ADMIN REGISTRATION
# ---------------------------
from django.contrib import admin

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "location", "job_type", "created_by", "category", "created_at")
    list_filter = ("job_type", "category")
    search_fields = ("title", "description", "location")

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "applicant", "job", "applied_at")
    search_fields = ("applicant__username", "job__title")
    list_filter = ("job",)
