from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job.title", read_only=True)
    applicant_name = serializers.CharField(source="applicant.username", read_only=True)
    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ["applicant", "ai_match_score", "status"]
