from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "posted_by", "location", "status", "created_at")
    list_filter = ("status", "remote", "employment_type")
    search_fields = ("title", "description")
