from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from apps.common.permissions import IsOwnerOrAdmin
from .models import Resume
from .serializers import ResumeUploadSerializer, ResumeSerializer
from .tasks import process_resume

class ResumeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_serializer_class(self):
        return ResumeUploadSerializer if self.action == "create" else ResumeSerializer

    def get_queryset(self):
        u = self.request.user
        if u.role == "admin":
            return Resume.objects.all()
        return Resume.objects.filter(user=u)

    def perform_create(self, serializer):
        resume = serializer.save(user=self.request.user)
        process_resume.delay(resume.id)  # async AI processing

    @action(detail=True, methods=["post"])
    def reanalyze(self, request, pk=None):
        resume = self.get_object()
        process_resume.delay(resume.id)
        return Response({"detail": "Re-analysis queued"}, status=status.HTTP_202_ACCEPTED)
