from django.db import models
from apps.common.models import TimeStampedModel
from apps.common.validators import validate_resume_file

class Resume(TimeStampedModel):
    class AnalysisStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        DONE = "done", "Done"
        FAILED = "failed", "Failed"

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="resumes")
    file = models.FileField(upload_to="resumes/", validators=[validate_resume_file])
    raw_text = models.TextField(blank=True)
    # Structured extraction
    parsed_data = models.JSONField(default=dict, blank=True)  # skills, experience, education, links
    # AI analysis output
    score = models.PositiveIntegerField(null=True, blank=True)  # 0-100
    strengths = models.JSONField(default=list, blank=True)
    weaknesses = models.JSONField(default=list, blank=True)
    skill_gaps = models.JSONField(default=list, blank=True)
    recommendations = models.JSONField(default=dict, blank=True)
    analysis_status = models.CharField(max_length=12, choices=AnalysisStatus.choices,
                                       default=AnalysisStatus.PENDING)
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
