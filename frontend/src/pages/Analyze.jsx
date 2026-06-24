import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import api from "../api/client";

export default function Analyze() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const qc = useQueryClient();

  const { data } = useQuery({
    queryKey: ["resumes"],
    queryFn: async () => (await api.get("/resumes/")).data.results || [],
    refetchInterval: (q) =>
      (q.state.data || []).some((r) => ["pending", "processing"].includes(r.analysis_status)) ? 3000 : false,
  });
  const latest = data?.[0];

  const upload = async () => {
    if (!file) return;
    setUploading(true);
    const fd = new FormData();
    fd.append("file", file);
    await api.post("/resumes/", fd, { headers: { "Content-Type": "multipart/form-data" } });
    setFile(null);
    qc.invalidateQueries({ queryKey: ["resumes"] });
    setUploading(false);
  };

  return (
    <div className="max-w-3xl mx-auto px-6 py-12">
      <h1 className="text-2xl font-bold mb-6">CV Upload & Analysis</h1>
      <div className="border-2 border-dashed rounded-lg p-8 text-center"
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => { e.preventDefault(); setFile(e.dataTransfer.files[0]); }}>
        <input type="file" accept=".pdf,.docx" onChange={(e) => setFile(e.target.files[0])} />
        <p className="text-sm text-gray-500 mt-2">{file ? file.name : "Drag & drop or select a PDF/DOCX"}</p>
        <button onClick={upload} disabled={!file || uploading}
          className="mt-4 px-5 py-2 bg-indigo-600 text-white rounded disabled:opacity-50">
          {uploading ? "Uploading…" : "Analyze"}
        </button>
      </div>

      {latest && (
        <div className="mt-10">
          <h2 className="text-lg font-semibold">Latest Analysis</h2>
          <p className="text-sm text-gray-500">Status: {latest.analysis_status}</p>
          {latest.analysis_status === "done" && (
            <div className="mt-4 space-y-4">
              <div className="text-4xl font-bold text-indigo-600">{latest.score}/100</div>
              <Section title="Strengths" items={latest.strengths} />
              <Section title="Weaknesses" items={latest.weaknesses} />
              <Section title="Skill Gaps" items={latest.skill_gaps} />
              <div>
                <h3 className="font-semibold">Suggested Roles</h3>
                <p className="text-gray-600 text-sm">
                  {(latest.recommendations?.suggested_roles || []).join(", ")}
                </p>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
function Section({ title, items }) {
  if (!items?.length) return null;
  return (
    <div>
      <h3 className="font-semibold">{title}</h3>
      <ul className="list-disc ml-5 text-sm text-gray-600">
        {items.map((x, i) => <li key={i}>{x}</li>)}
      </ul>
    </div>
  );
}
