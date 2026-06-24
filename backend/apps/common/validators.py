import os
from django.conf import settings
from django.core.exceptions import ValidationError

def validate_resume_file(file):
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in settings.ALLOWED_RESUME_EXTENSIONS:
        raise ValidationError(f"Unsupported file type {ext}. Allowed: {settings.ALLOWED_RESUME_EXTENSIONS}")
    if file.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError("File too large (max 10MB).")
