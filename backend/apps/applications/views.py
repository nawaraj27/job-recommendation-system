from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Application
from .serializers import ApplicationSerializer
from apps.ai_engine.agents import run_job_matching

class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        u = self.request.user
        if u.role == "admin":
            return Application.objects.all()
        if u.role == "member":
            return Application.objects.filter(job__posted_by=u)  # applicants to my jobs
        return Application.objects.filter(applicant=u)           # my own applications

    def perform_create(self, serializer):
        app = serializer.save(applicant=self.request.user, status=Application.Status.SCREENING)
        # AI pre-screen
        skills = app.resume.parsed_data.get("skills", []) if app.resume else []
        jobs = [{"id": app.job.id, "title": app.job.title,
                 "required_skills": app.job.required_skills}]
        res = run_job_matching(skills, jobs)
        matches = res.get("matches", [])
        if matches:
            app.ai_match_score = matches[0].get("score")
        app.status = Application.Status.SUBMITTED
        app.save(update_fields=["ai_match_score", "status"])

    @action(detail=True, methods=["post"])
    def decide(self, request, pk=None):
        """Member/admin accepts or rejects an application."""
        app = self.get_object()
        if request.user.role not in ("member", "admin"):
            return Response({"detail": "Not allowed"}, status=403)
        decision = request.data.get("status")
        if decision not in ("accepted", "rejected", "reviewed"):
            return Response({"detail": "Invalid status"}, status=400)
        app.status = decision
        app.save(update_fields=["status"])
        return Response(ApplicationSerializer(app).data)
