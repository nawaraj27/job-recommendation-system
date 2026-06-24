from rest_framework import serializers
from .models import InterviewSession, PromptTemplate

class InterviewSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewSession
        fields = "__all__"
        read_only_fields = ["user", "questions", "answers", "overall_score"]

class PromptTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptTemplate
        fields = "__all__"
