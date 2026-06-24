from rest_framework import serializers
from .models import Resume

class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ["id", "file", "analysis_status", "created_at"]
        read_only_fields = ["analysis_status"]

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = "__all__"
        read_only_fields = ["user", "raw_text", "parsed_data", "score", "strengths",
                            "weaknesses", "skill_gaps", "recommendations",
                            "analysis_status", "error_message"]
