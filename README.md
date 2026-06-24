# AI Skill Analyzer Platform

Full-stack AI career intelligence platform: CV upload & parsing, AI skill scoring,
interview simulation, job matching, CV builder, and company member onboarding with
admin approval.

## Stack
- **Backend:** Django 5 + DRF, PostgreSQL, Celery + Redis, SimpleJWT, drf-spectacular
- **AI:** Google Gemini + LangGraph agents (Resume Analysis, Job Matching, Interview, Career Advisor) with offline heuristic fallback
- **Frontend:** React (Vite) + Tailwind + React Router + React Query + Zustand
- **Infra:** Docker Compose + Nginx

## Backend apps
`users` · `jobs` · `resumes` · `ai_engine` · `applications` · `cms` (+ `common` for RBAC/audit)

## Quick start (Docker)
```bash
cp backend/.env.example backend/.env   # set GEMINI_API_KEY (optional; works without it)
docker compose up --build
```
Then:
```bash
docker compose exec backend python manage.py createsuperuser
docker compose exec backend python manage.py seed_cms   # populate dynamic site content
```
- Frontend: http://localhost (via Nginx) or http://localhost:5173
- API docs: http://localhost:8000/api/docs/
- Admin: http://localhost:8000/admin/

## Local dev (without Docker)
Backend:
```bash
cd backend && python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate && python manage.py seed_cms
python manage.py runserver
# separate terminal:
celery -A config worker -l info
```
Frontend:
```bash
cd frontend && npm install && npm run dev
```

## Key API endpoints
| Area | Endpoint |
|------|----------|
| Register / Login / Refresh | `POST /api/auth/register/` `login/` `refresh/` |
| Member verification | `POST /api/auth/member/verify/` |
| Admin approve member | `PATCH /api/auth/admin/members/{id}/` |
| Jobs CRUD + filters | `/api/jobs/` |
| Resume upload + analysis | `POST /api/resumes/` (async via Celery) |
| Job matching | `POST /api/ai/match-jobs/` |
| Interview create / submit | `/api/ai/interviews/` , `…/submit/` |
| Applications + decide | `/api/applications/` , `…/decide/` |
| CMS content by group | `GET /api/cms/content/group/{group}/` |

## Notes
- Frontend has **no hardcoded marketing text** — all content comes from the CMS (`seed_cms` seeds defaults; edit in Django admin).
- AI works **without an API key** using heuristic fallbacks, so the platform is runnable end-to-end immediately. Set `GEMINI_API_KEY` for real LLM analysis.
- RBAC enforced via `apps/common/permissions.py`; mutating API calls logged via `AuditLogMiddleware`.

## What's scaffolded vs. TODO
Done: auth+RBAC, all models/migrations-ready apps, resume parsing, async AI pipeline,
agent layer, job/application flows, member approval workflow, CMS, Docker.
Next: real PDF export for CV builder, S3 wiring (toggle `USE_S3`), anti-malware scan
hook on upload, embeddings-based semantic matching, GitHub Actions CI, richer admin analytics.
