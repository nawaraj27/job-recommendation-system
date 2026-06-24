from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import JobMatchView, InterviewViewSet, PromptTemplateViewSet

router = DefaultRouter()
router.register("interviews", InterviewViewSet, basename="interview")
router.register("prompts", PromptTemplateViewSet, basename="prompt")

urlpatterns = [
    path("match-jobs/", JobMatchView.as_view({"post": "create"})),
] + router.urls
