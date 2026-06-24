import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import api from "../api/client";
import { useAuth } from "../store/auth";

export default function Dashboard() {
  const { user } = useAuth();
  return (
    <div className="max-w-4xl mx-auto px-6 py-12">
      <h1 className="text-2xl font-bold mb-2">Dashboard</h1>
      <p className="text-gray-500 mb-8">Signed in as {user.username} ({user.role})</p>
      {user.role === "user" && <UserDash />}
      {user.role === "member" && <MemberDash user={user} />}
      {user.role === "admin" && <AdminDash />}
    </div>
  );
}

function UserDash() {
  const nav = useNavigate();
  const { data: apps } = useQuery({
    queryKey: ["myApps"], queryFn: async () => (await api.get("/applications/")).data.results || [],
  });
  const startInterview = async () => {
    const { data } = await api.post("/ai/interviews/", { role: "Software Engineer" });
    nav(`/interview/${data.id}`);
  };
  return (
    <div className="space-y-4">
      <div className="flex gap-3">
        <button onClick={() => nav("/analyze")} className="px-4 py-2 bg-indigo-600 text-white rounded">Analyze CV</button>
        <button onClick={startInterview} className="px-4 py-2 border rounded">Start Interview</button>
      </div>
      <h2 className="font-semibold mt-6">My Applications</h2>
      {(apps || []).map((a) => (
        <div key={a.id} className="border rounded p-3 text-sm">{a.job_title} — {a.status} (match {a.ai_match_score ?? "—"})</div>
      ))}
    </div>
  );
}

function MemberDash({ user }) {
  const [job, setJob] = useState({ title: "", description: "", location: "", required_skills: "" });
  const set = (k) => (e) => setJob({ ...job, [k]: e.target.value });
  const { data: apps } = useQuery({
    queryKey: ["jobApps"], queryFn: async () => (await api.get("/applications/")).data.results || [],
  });
  const postJob = async () => {
    await api.post("/jobs/", { ...job, required_skills: job.required_skills.split(",").map((s) => s.trim()) });
    alert("Job posted");
  };
  if (!user.is_approved) {
    return <VerifyUpload />;
  }
  return (
    <div className="space-y-4">
      <h2 className="font-semibold">Post a Job</h2>
      <input placeholder="Title" value={job.title} onChange={set("title")} className="border rounded w-full px-3 py-2" />
      <textarea placeholder="Description" value={job.description} onChange={set("description")} className="border rounded w-full px-3 py-2" />
      <input placeholder="Location" value={job.location} onChange={set("location")} className="border rounded w-full px-3 py-2" />
      <input placeholder="Required skills (comma separated)" value={job.required_skills} onChange={set("required_skills")} className="border rounded w-full px-3 py-2" />
      <button onClick={postJob} className="px-4 py-2 bg-indigo-600 text-white rounded">Post Job</button>
      <h2 className="font-semibold mt-6">Applicants</h2>
      {(apps || []).map((a) => (
        <div key={a.id} className="border rounded p-3 text-sm flex justify-between">
          <span>{a.applicant_name} → {a.job_title} (match {a.ai_match_score ?? "—"})</span>
          <span className="text-gray-500">{a.status}</span>
        </div>
      ))}
    </div>
  );
}

function VerifyUpload() {
  const [files, setFiles] = useState({});
  const submit = async () => {
    const fd = new FormData();
    if (files.citizenship_doc) fd.append("citizenship_doc", files.citizenship_doc);
    if (files.company_certificate) fd.append("company_certificate", files.company_certificate);
    if (files.business_doc) fd.append("business_doc", files.business_doc);
    await api.post("/auth/member/verify/", fd, { headers: { "Content-Type": "multipart/form-data" } });
    alert("Documents submitted. Await admin approval.");
  };
  return (
    <div className="space-y-3">
      <p className="text-amber-600">Your member account is pending approval. Upload verification documents:</p>
      {["citizenship_doc", "company_certificate", "business_doc"].map((f) => (
        <div key={f}>
          <label className="text-sm capitalize">{f.replace(/_/g, " ")}</label>
          <input type="file" onChange={(e) => setFiles({ ...files, [f]: e.target.files[0] })} className="block" />
        </div>
      ))}
      <button onClick={submit} className="px-4 py-2 bg-indigo-600 text-white rounded">Submit for Approval</button>
    </div>
  );
}

function AdminDash() {
  const { data: pending, refetch } = useQuery({
    queryKey: ["pendingMembers"], queryFn: async () => (await api.get("/auth/admin/members/")).data.results || [],
  });
  const decide = async (id, status) => {
    await api.patch(`/auth/admin/members/${id}/`, { status });
    refetch();
  };
  return (
    <div className="space-y-3">
      <h2 className="font-semibold">Pending Member Approvals</h2>
      {(pending || []).filter((m) => m.status === "pending").map((m) => (
        <div key={m.id} className="border rounded p-3 flex justify-between items-center text-sm">
          <span>Verification #{m.id}</span>
          <span className="flex gap-2">
            <button onClick={() => decide(m.id, "approved")} className="px-3 py-1 bg-green-600 text-white rounded">Approve</button>
            <button onClick={() => decide(m.id, "rejected")} className="px-3 py-1 bg-red-500 text-white rounded">Reject</button>
          </span>
        </div>
      ))}
      <p className="text-sm text-gray-500 mt-4">Full content/CMS, jobs, and AI-prompt management available in Django admin at /admin/.</p>
    </div>
  );
}
