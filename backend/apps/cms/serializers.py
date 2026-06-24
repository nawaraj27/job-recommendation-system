from rest_framework import serializers
from .models import SiteContent, TeamMember, CVTemplate

class SiteContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteContent
        fields = ["key", "value", "group"]

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = "__all__"

class CVTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVTemplate
        fields = "__all__"
