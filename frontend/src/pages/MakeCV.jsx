import { useState } from "react";
import api from "../api/client";

export default function MakeCV() {
  const [mode, setMode] = useState("manual");
  const [form, setForm] = useState({ name: "", title: "", skills: "", experience: "", education: "" });
  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  return (
    <div className="max-w-3xl mx-auto px-6 py-12">
      <h1 className="text-2xl font-bold mb-2">CV Maker</h1>
      <div className="flex gap-3 mb-6">
        <button onClick={() => setMode("manual")}
          className={`px-4 py-2 rounded ${mode === "manual" ? "bg-indigo-600 text-white" : "border"}`}>Manual</button>
        <button onClick={() => setMode("ai")}
          className={`px-4 py-2 rounded ${mode === "ai" ? "bg-indigo-600 text-white" : "border"}`}>AI-Assisted</button>
      </div>
      <div className="space-y-3">
        {["name", "title", "skills", "experience", "education"].map((f) => (
          <input key={f} value={form[f]} onChange={set(f)} placeholder={f}
            className="border rounded w-full px-3 py-2 capitalize" />
        ))}
      </div>
      <p className="text-sm text-gray-500 mt-4">
        {mode === "ai"
          ? "AI mode will format and enhance your CV, then export a PDF."
          : "Fill the sections, then export your CV as PDF."}
      </p>
      <button className="mt-4 px-6 py-3 bg-indigo-600 text-white rounded">
        {mode === "ai" ? "Generate with AI" : "Build CV"}
      </button>
    </div>
  );
}
