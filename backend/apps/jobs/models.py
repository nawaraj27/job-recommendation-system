from django.db import models
from apps.common.models import TimeStampedModel

class Job(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        OPEN = "open", "Open"
        CLOSED = "closed", "Closed"

    posted_by = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True)
    remote = models.BooleanField(default=False)
    employment_type = models.CharField(max_length=50, blank=True)  # full-time etc.
    salary_min = models.PositiveIntegerField(null=True, blank=True)
    salary_max = models.PositiveIntegerField(null=True, blank=True)
    required_skills = models.JSONField(default=list, blank=True)  # ["python","react"]
    experience_years = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
