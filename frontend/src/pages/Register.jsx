import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../store/auth";

export default function Register() {
  const { register } = useAuth(); const nav = useNavigate();
  const [form, setForm] = useState({ username: "", email: "", password: "", role: "user", company_name: "" });
  const [err, setErr] = useState("");
  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  const submit = async () => {
    try { await register(form); nav(form.role === "member" ? "/dashboard" : "/dashboard"); }
    catch (e) { setErr(JSON.stringify(e.response?.data || "Registration failed")); }
  };

  return (
    <div className="max-w-sm mx-auto px-6 py-16">
      <h1 className="text-2xl font-bold mb-6">Register</h1>
      {err && <p className="text-red-500 text-sm mb-3">{err}</p>}
      <select value={form.role} onChange={set("role")} className="border rounded w-full px-3 py-2 mb-3">
        <option value="user">Normal User</option>
        <option value="member">Company / Member</option>
      </select>
      <input value={form.username} onChange={set("username")} placeholder="Username" className="border rounded w-full px-3 py-2 mb-3" />
      <input value={form.email} onChange={set("email")} placeholder="Email" className="border rounded w-full px-3 py-2 mb-3" />
      {form.role === "member" && (
        <input value={form.company_name} onChange={set("company_name")} placeholder="Company name" className="border rounded w-full px-3 py-2 mb-3" />
      )}
      <input type="password" value={form.password} onChange={set("password")} placeholder="Password" className="border rounded w-full px-3 py-2 mb-4" />
      <button onClick={submit} className="w-full py-2 bg-indigo-600 text-white rounded">Create account</button>
      {form.role === "member" && (
        <p className="text-xs text-gray-500 mt-3">After registering, upload verification documents from your dashboard. An admin must approve before you can post jobs.</p>
      )}
    </div>
  );
}
