from celery import shared_task
from .models import Resume
from .extractor import extract_text, extract_links
from apps.ai_engine.agents import run_resume_analysis

@shared_task
def process_resume(resume_id):
    try:
        resume = Resume.objects.get(id=resume_id)
    except Resume.DoesNotExist:
        return
    resume.analysis_status = Resume.AnalysisStatus.PROCESSING
    resume.save(update_fields=["analysis_status"])
    try:
        text = extract_text(resume.file.path)
        resume.raw_text = text
        links = extract_links(text)
        result = run_resume_analysis(text)          # AI agent (Gemini/LangGraph)
        parsed = result.get("parsed", {})
        parsed["links"] = links
        resume.parsed_data = parsed
        resume.score = result.get("score")
        resume.strengths = result.get("strengths", [])
        resume.weaknesses = result.get("weaknesses", [])
        resume.skill_gaps = result.get("skill_gaps", [])
        resume.recommendations = result.get("recommendations", {})
        resume.analysis_status = Resume.AnalysisStatus.DONE
        resume.save()
    except Exception as e:
        resume.analysis_status = Resume.AnalysisStatus.FAILED
        resume.error_message = str(e)
        resume.save(update_fields=["analysis_status", "error_message"])
