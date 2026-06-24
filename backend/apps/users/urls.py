from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (RegisterView, LoginView, MeView,
                    MemberVerificationView, AdminMemberViewSet)

admin_list = AdminMemberViewSet.as_view({"get": "list"})
admin_detail = AdminMemberViewSet.as_view({"get": "retrieve", "patch": "partial_update"})

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("me/", MeView.as_view()),
    path("member/verify/", MemberVerificationView.as_view()),
    path("admin/members/", admin_list),
    path("admin/members/<int:pk>/", admin_detail),
]
