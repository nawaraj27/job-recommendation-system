from django.contrib import admin
from .models import PromptTemplate, InterviewSession, AIUsageLog

@admin.register(PromptTemplate)
class PromptTemplateAdmin(admin.ModelAdmin):
    list_display = ("key", "description", "updated_at")

@admin.register(InterviewSession)
class InterviewSessionAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "overall_score", "created_at")

@admin.register(AIUsageLog)
class AIUsageLogAdmin(admin.ModelAdmin):
    list_display = ("user", "operation", "created_at")
    list_filter = ("operation",)
