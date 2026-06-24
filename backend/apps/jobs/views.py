from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from apps.common.permissions import ReadOnlyOrApprovedMember, IsOwnerOrAdmin
from .models import Job
from .serializers import JobSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.filter(status="open")
    serializer_class = JobSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["location", "remote", "employment_type", "experience_years"]
    search_fields = ["title", "description", "required_skills"]
    ordering_fields = ["created_at", "salary_max"]

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        if self.action == "create":
            return [ReadOnlyOrApprovedMember()]
        return [IsOwnerOrAdmin()]

    def get_queryset(self):
        # Members/admin see their own incl. drafts; public sees open only
        u = self.request.user
        if u.is_authenticated and u.role == "admin":
            return Job.objects.all()
        if u.is_authenticated and u.role == "member":
            return Job.objects.filter(status="open") | Job.objects.filter(posted_by=u)
        return Job.objects.filter(status="open")

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)
