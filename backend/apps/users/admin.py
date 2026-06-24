from django.contrib import admin
from .models import User, MemberVerification

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_approved", "company_name")
    list_filter = ("role", "is_approved")
    search_fields = ("username", "email", "company_name")

@admin.register(MemberVerification)
class MemberVerificationAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "reviewed_by", "created_at")
    list_filter = ("status",)
