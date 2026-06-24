from django.core.management.base import BaseCommand
from apps.cms.models import SiteContent

CONTENT = {
    "home": {
        "home.nav.logo": {"text": "SkillAnalyzer"},
        "home.hero.title": {"text": "Analyze Your Skills. Land Your Dream Job."},
        "home.hero.subtitle": {"text": "Upload your CV and let AI score your skills, "
                                        "simulate interviews, and match you with jobs."},
        "home.hero.cta": {"text": "Start Skill Analysis"},
        "home.features": {"items": [
            {"title": "AI CV Scoring", "desc": "Get a 0-100 score with strengths & gaps."},
            {"title": "Job Matching", "desc": "AI ranks jobs that fit your profile."},
            {"title": "Interview Simulation", "desc": "Practice with AI-generated questions."},
            {"title": "CV Builder", "desc": "Build a professional CV, manual or AI-assisted."},
        ]},
    },
    "about": {
        "about.mission": {"text": "To make career growth intelligent and accessible."},
        "about.vision": {"text": "A world where every professional is matched to the right role."},
        "about.platform": {"text": "We use AI agents to read resumes, evaluate skills, and connect talent with companies."},
    },
    "footer": {
        "footer.contact": {"email": "hello@skillanalyzer.com", "phone": "+1-000-000-0000"},
        "footer.social": {"linkedin": "#", "twitter": "#", "github": "#"},
    },
    "legal": {
        "legal.terms": {"text": "Terms of Service content managed via admin."},
        "legal.privacy": {"text": "Privacy Policy content managed via admin."},
    },
}

class Command(BaseCommand):
    help = "Seed CMS site content so frontend has no hardcoded text."

    def handle(self, *args, **opts):
        n = 0
        for group, entries in CONTENT.items():
            for key, value in entries.items():
                SiteContent.objects.update_or_create(
                    key=key, defaults={"value": value, "group": group})
                n += 1
        self.stdout.write(self.style.SUCCESS(f"Seeded {n} CMS entries."))
