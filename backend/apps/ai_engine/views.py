from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.common.permissions import IsAdmin
from apps.jobs.models import Job
from apps.resumes.models import Resume
from .models import InterviewSession, PromptTemplate, AIUsageLog
from .serializers import InterviewSessionSerializer, PromptTemplateSerializer
from .agents import (run_job_matching, run_interview_questions, run_answer_evaluation)

class JobMatchView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """Match the user's latest analyzed resume against open jobs."""
        resume = Resume.objects.filter(user=request.user, analysis_status="done").first()
        if not resume:
            return Response({"detail": "No analyzed resume found."}, status=400)
        skills = resume.parsed_data.get("skills", [])
        jobs = list(Job.objects.filter(status="open").values("id", "title", "required_skills"))
        result = run_job_matching(skills, jobs)
        AIUsageLog.objects.create(user=request.user, operation="job_match")
        # attach titles
        title_map = {j["id"]: j["title"] for j in jobs}
        for m in result.get("matches", []):
            m["title"] = title_map.get(m["job_id"], "")
        return Response(result)

class InterviewViewSet(viewsets.ModelViewSet):
    serializer_class = InterviewSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InterviewSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        session = serializer.save(user=self.request.user)
        resume = session.resume or Resume.objects.filter(
            user=self.request.user, analysis_status="done").first()
        skills = resume.parsed_data.get("skills", []) if resume else []
        q = run_interview_questions(session.role or "Software Engineer", skills)
        session.questions = q.get("questions", [])
        session.save(update_fields=["questions"])
        AIUsageLog.objects.create(user=self.request.user, operation="interview_questions")

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        """Submit answers: [{question, answer}]. Returns scored feedback."""
        session = self.get_object()
        answers_in = request.data.get("answers", [])
        scored, total = [], 0
        for a in answers_in:
            ev = run_answer_evaluation(a.get("question", ""), a.get("answer", ""))
            entry = {**a, **ev}
            scored.append(entry)
            total += ev.get("score", 0)
        session.answers = scored
        session.overall_score = int(total / len(scored)) if scored else 0
        session.save(update_fields=["answers", "overall_score"])
        AIUsageLog.objects.create(user=request.user, operation="answer_evaluation")
        return Response(InterviewSessionSerializer(session).data)

class PromptTemplateViewSet(viewsets.ModelViewSet):
    queryset = PromptTemplate.objects.all()
    serializer_class = PromptTemplateSerializer
    permission_classes = [IsAdmin]
