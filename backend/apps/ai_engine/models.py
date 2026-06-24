from django.db import models
from apps.common.models import TimeStampedModel

class PromptTemplate(TimeStampedModel):
    """Admin-editable AI prompts."""
    key = models.CharField(max_length=64, unique=True)
    template = models.TextField()
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.key

class InterviewSession(TimeStampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="interviews")
    resume = models.ForeignKey("resumes.Resume", null=True, blank=True, on_delete=models.SET_NULL)
    role = models.CharField(max_length=255, blank=True)
    questions = models.JSONField(default=list)   # [{type, question}]
    answers = models.JSONField(default=list)     # [{question, answer, score, feedback}]
    overall_score = models.PositiveIntegerField(null=True, blank=True)

class AIUsageLog(TimeStampedModel):
    user = models.ForeignKey("users.User", null=True, on_delete=models.SET_NULL)
    operation = models.CharField(max_length=64)  # resume_analysis, job_match, etc.
    tokens = models.PositiveIntegerField(default=0)
