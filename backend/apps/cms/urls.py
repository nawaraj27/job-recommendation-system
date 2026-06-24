from rest_framework.routers import DefaultRouter
from .views import SiteContentViewSet, TeamMemberViewSet, CVTemplateViewSet
router = DefaultRouter()
router.register("content", SiteContentViewSet, basename="content")
router.register("team", TeamMemberViewSet, basename="team")
router.register("cv-templates", CVTemplateViewSet, basename="cvtemplate")
urlpatterns = router.urls
