"""Agent orchestration. Uses LangGraph if available; otherwise sequential fallback.

Agents:
  - Resume Analysis Agent
  - Job Matching Agent
  - Interview Agent
  - Career Advisor Agent (folded into resume recommendations)
"""
from . import prompts
from .gemini_client import generate_json
from .prompts import RESUME_ANALYSIS, JOB_MATCHING, INTERVIEW_QUESTIONS, ANSWER_EVALUATION

# ---- Heuristic fallback so the platform works without an API key ----
_COMMON_SKILLS = ["python", "django", "react", "javascript", "sql", "docker",
                  "aws", "node", "typescript", "java", "git", "rest", "celery"]

def _heuristic_resume(text):
    low = text.lower()
    found = sorted({s for s in _COMMON_SKILLS if s in low})
    score = min(100, 40 + len(found) * 5)
    return {
        "parsed": {"skills": found, "experience": [], "education": [], "projects": []},
        "score": score,
        "strengths": [f"Demonstrates {s}" for s in found[:3]],
        "weaknesses": ["Add quantifiable achievements"] if score < 80 else [],
        "skill_gaps": [s for s in ["docker", "aws", "typescript"] if s not in found][:3],
        "recommendations": {
            "suggested_roles": ["Software Engineer"] if found else ["Junior Developer"],
            "career_path": "Backend → Senior Backend → Tech Lead",
            "learning": ["System design", "Cloud fundamentals"],
        },
    }

def run_resume_analysis(resume_text):
    return generate_json(
        RESUME_ANALYSIS.format(resume_text=resume_text[:12000]),
        fallback=_heuristic_resume(resume_text),
    )

def run_job_matching(skills, jobs):
    """jobs: list of {id, title, required_skills}. Returns ranked matches."""
    fallback = {"matches": []}
    skillset = set(s.lower() for s in skills)
    for j in jobs:
        req = set(s.lower() for s in (j.get("required_skills") or []))
        overlap = len(skillset & req)
        denom = len(req) or 1
        fallback["matches"].append({
            "job_id": j["id"],
            "score": int(overlap / denom * 100),
            "reason": f"{overlap}/{denom} required skills matched",
        })
    fallback["matches"].sort(key=lambda m: m["score"], reverse=True)
    return generate_json(JOB_MATCHING.format(skills=skills, jobs=jobs), fallback=fallback)

def run_interview_questions(role, skills, count=5):
    fallback = {"questions": [
        {"type": "technical", "question": f"Explain a project where you used {skills[0] if skills else 'your main skill'}."},
        {"type": "behavioral", "question": "Describe a time you handled a tight deadline."},
        {"type": "role-specific", "question": f"What makes you a fit for a {role} role?"},
    ][:count]}
    return generate_json(
        INTERVIEW_QUESTIONS.format(count=count, role=role, skills=skills),
        fallback=fallback,
    )

def run_answer_evaluation(question, answer):
    fallback = {
        "score": min(100, 40 + len(answer.split())),
        "feedback": "Answer recorded. Add specific examples and measurable outcomes.",
        "improvements": ["Use the STAR method", "Quantify your impact"],
    }
    return generate_json(
        ANSWER_EVALUATION.format(question=question, answer=answer),
        fallback=fallback,
    )
