from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.common.models import TimeStampedModel

class User(AbstractUser):
    class Role(models.TextChoices):
        USER = "user", "Normal User"
        MEMBER = "member", "Company Member"
        ADMIN = "admin", "Admin"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)
    phone = models.CharField(max_length=30, blank=True)
    # Member/company fields
    company_name = models.CharField(max_length=255, blank=True)
    is_approved = models.BooleanField(default=False)  # admin approval for members

    def save(self, *args, **kwargs):
        if self.role == self.Role.ADMIN:
            self.is_staff = True
        super().save(*args, **kwargs)

class MemberVerification(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="verification")
    citizenship_doc = models.FileField(upload_to="verifications/citizenship/")
    company_certificate = models.FileField(upload_to="verifications/certificates/")
    business_doc = models.FileField(upload_to="verifications/business/", blank=True, null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    rejection_reason = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="reviews")
