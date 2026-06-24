from django.db import models
from apps.common.models import TimeStampedModel

class SiteContent(TimeStampedModel):
    """Generic key/value CMS blocks. key e.g. 'home.hero.title'. Frontend has NO hardcoded text."""
    key = models.CharField(max_length=128, unique=True)
    value = models.JSONField(default=dict)  # supports rich/structured content
    group = models.CharField(max_length=64, blank=True)  # home, about, footer, legal

    def __str__(self):
        return self.key

class TeamMember(TimeStampedModel):
    name = models.CharField(max_length=128)
    role = models.CharField(max_length=128)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="team/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

class CVTemplate(TimeStampedModel):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=255, blank=True)
    structure = models.JSONField(default=dict)  # sections/layout definition
    is_active = models.BooleanField(default=True)
