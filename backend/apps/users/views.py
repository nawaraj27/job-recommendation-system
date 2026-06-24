from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.common.permissions import IsAdmin
from .models import User, MemberVerification
from .serializers import (RegisterSerializer, UserSerializer,
                          MemberVerificationSerializer, MyTokenObtainPairSerializer)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    throttle_scope = "auth"

class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    throttle_scope = "auth"

class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user

class MemberVerificationView(generics.CreateAPIView):
    serializer_class = MemberVerificationSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AdminMemberViewSet(viewsets.ModelViewSet):
    """Admin: approve/reject member verifications and manage users."""
    queryset = MemberVerification.objects.select_related("user").all()
    serializer_class = MemberVerificationSerializer
    permission_classes = [IsAdmin]

    def partial_update(self, request, *args, **kwargs):
        obj = self.get_object()
        new_status = request.data.get("status")
        if new_status in ("approved", "rejected"):
            obj.status = new_status
            obj.rejection_reason = request.data.get("rejection_reason", "")
            obj.reviewed_by = request.user
            obj.save()
            if new_status == "approved":
                obj.user.is_approved = True
                obj.user.save()
            return Response(self.get_serializer(obj).data)
        return Response({"detail": "status must be approved or rejected"},
                        status=status.HTTP_400_BAD_REQUEST)
