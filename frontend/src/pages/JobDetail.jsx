import { useParams, useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import api from "../api/client";
import { useAuth } from "../store/auth";

export default function JobDetail() {
  const { id } = useParams();
  const nav = useNavigate();
  const { user } = useAuth();
  const { data: job } = useQuery({
    queryKey: ["job", id],
    queryFn: async () => (await api.get(`/jobs/${id}/`)).data,
  });
  if (!job) return <div className="p-12 text-gray-400">Loading…</div>;

  const apply = async () => {
    if (!user) return nav("/login");
    const resumes = (await api.get("/resumes/")).data.results || [];
    const resumeId = resumes[0]?.id || null;
    await api.post("/applications/", { job: job.id, resume: resumeId });
    alert("Application submitted!");
  };

  return (
    <div className="max-w-3xl mx-auto px-6 py-12">
      <h1 className="text-3xl font-bold">{job.title}</h1>
      <p className="text-gray-500 mt-1">{job.company_name} · {job.location || "Remote"}</p>
      <p className="mt-6 whitespace-pre-line text-gray-700">{job.description}</p>
      {job.required_skills?.length > 0 && (
        <div className="mt-6 flex flex-wrap gap-2">
          {job.required_skills.map((s) => (
            <span key={s} className="px-2 py-1 bg-indigo-50 text-indigo-700 rounded text-xs">{s}</span>
          ))}
        </div>
      )}
      <button onClick={apply} className="mt-8 px-6 py-3 bg-indigo-600 text-white rounded-lg">
        Apply with my CV
      </button>
    </div>
  );
}
