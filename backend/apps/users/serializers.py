from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from .models import User, MemberVerification

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name",
                  "role", "phone", "company_name", "is_approved"]
        read_only_fields = ["role", "is_approved"]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    role = serializers.ChoiceField(choices=[("user", "user"), ("member", "member")], default="user")

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name",
                  "phone", "company_name", "role"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class MemberVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberVerification
        fields = ["id", "citizenship_doc", "company_certificate", "business_doc",
                  "status", "rejection_reason", "created_at"]
        read_only_fields = ["status", "rejection_reason"]

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["is_approved"] = user.is_approved
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data
        return data
