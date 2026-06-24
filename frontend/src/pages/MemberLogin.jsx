import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../store/auth";

export default function MemberLogin() {
  const [u, setU] = useState(""); const [p, setP] = useState(""); const [err, setErr] = useState("");
  const { login } = useAuth(); const nav = useNavigate();
  const submit = async () => {
    try {
      const user = await login(u, p);
      if (user.role !== "member") { setErr("Not a member account"); return; }
      nav("/dashboard");
    } catch { setErr("Invalid credentials"); }
  };
  return (
    <div className="max-w-sm mx-auto px-6 py-16">
      <h1 className="text-2xl font-bold mb-2">Member Login</h1>
      <p className="text-sm text-gray-500 mb-6">For approved company accounts.</p>
      {err && <p className="text-red-500 text-sm mb-3">{err}</p>}
      <input value={u} onChange={(e) => setU(e.target.value)} placeholder="Username"
        className="border rounded w-full px-3 py-2 mb-3" />
      <input type="password" value={p} onChange={(e) => setP(e.target.value)} placeholder="Password"
        className="border rounded w-full px-3 py-2 mb-4" />
      <button onClick={submit} className="w-full py-2 bg-indigo-600 text-white rounded">Login</button>
    </div>
  );
}
