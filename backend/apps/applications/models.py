from django.db import models
from apps.common.models import TimeStampedModel

class Application(TimeStampedModel):
    class Status(models.TextChoices):
        SUBMITTED = "submitted", "Submitted"
        SCREENING = "screening", "AI Screening"
        REVIEWED = "reviewed", "Reviewed"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    applicant = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="applications")
    job = models.ForeignKey("jobs.Job", on_delete=models.CASCADE, related_name="applications")
    resume = models.ForeignKey("resumes.Resume", null=True, blank=True, on_delete=models.SET_NULL)
    cover_letter = models.TextField(blank=True)
    ai_match_score = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.SUBMITTED)

    class Meta:
        unique_together = ("applicant", "job")
        ordering = ["-created_at"]
