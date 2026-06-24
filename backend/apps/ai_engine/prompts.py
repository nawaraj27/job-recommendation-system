"""Centralized, admin-editable prompt templates (override via PromptTemplate model)."""

RESUME_ANALYSIS = """You are a senior technical recruiter. Analyze the resume text below.
Return STRICT JSON only with this shape:
{{
 "parsed": {{"skills": [], "experience": [], "education": [], "projects": []}},
 "score": <0-100 integer>,
 "strengths": [],
 "weaknesses": [],
 "skill_gaps": [],
 "recommendations": {{"suggested_roles": [], "career_path": "", "learning": []}}
}}
Resume:
\"\"\"{resume_text}\"\"\""""

JOB_MATCHING = """Given a candidate's skills {skills} and these jobs {jobs},
rank the jobs by suitability. Return STRICT JSON:
{{"matches": [{{"job_id": <id>, "score": <0-100>, "reason": ""}}]}}"""

INTERVIEW_QUESTIONS = """Generate {count} interview questions for role "{role}" based on
candidate skills {skills}. Mix technical, behavioral, and role-specific.
Return STRICT JSON: {{"questions": [{{"type": "", "question": ""}}]}}"""

ANSWER_EVALUATION = """Evaluate this interview answer.
Question: {question}
Answer: {answer}
Return STRICT JSON: {{"score": <0-100>, "feedback": "", "improvements": []}}"""
