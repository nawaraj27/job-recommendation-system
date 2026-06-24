from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.common.permissions import IsAdmin
from .models import SiteContent, TeamMember, CVTemplate
from .serializers import SiteContentSerializer, TeamMemberSerializer, CVTemplateSerializer

class SiteContentViewSet(viewsets.ModelViewSet):
    queryset = SiteContent.objects.all()
    serializer_class = SiteContentSerializer
    lookup_field = "key"

    def get_permissions(self):
        return [AllowAny()] if self.action in ("list", "retrieve", "by_group") else [IsAdmin()]

    @action(detail=False, methods=["get"], url_path="group/(?P<group>[^/.]+)")
    def by_group(self, request, group=None):
        qs = self.queryset.filter(group=group)
        data = {c.key: c.value for c in qs}
        return Response(data)

class TeamMemberViewSet(viewsets.ModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    def get_permissions(self):
        return [AllowAny()] if self.action in ("list", "retrieve") else [IsAdmin()]

class CVTemplateViewSet(viewsets.ModelViewSet):
    queryset = CVTemplate.objects.filter(is_active=True)
    serializer_class = CVTemplateSerializer
    def get_permissions(self):
        return [AllowAny()] if self.action in ("list", "retrieve") else [IsAdmin()]
