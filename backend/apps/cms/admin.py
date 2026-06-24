from django.contrib import admin
from .models import SiteContent, TeamMember, CVTemplate

@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ("key", "group", "updated_at")
    list_filter = ("group",)
    search_fields = ("key",)

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order")

@admin.register(CVTemplate)
class CVTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
