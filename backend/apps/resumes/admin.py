from django.contrib import admin
from .models import Resume

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("user", "score", "analysis_status", "created_at")
    list_filter = ("analysis_status",)
