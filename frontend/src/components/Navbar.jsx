import { Link, useNavigate } from "react-router-dom";
import { useCmsGroup } from "../api/cms";
import { useAuth } from "../store/auth";

export default function Navbar() {
  const { data: cms } = useCmsGroup("home");
  const { user, logout } = useAuth();
  const nav = useNavigate();
  const logo = cms?.["home.nav.logo"]?.text || "...";

  return (
    <nav className="flex items-center justify-between px-6 py-4 border-b bg-white">
      <Link to="/" className="text-xl font-bold text-indigo-600">{logo}</Link>
      <div className="flex items-center gap-5 text-sm">
        <Link to="/">Home</Link>
        <Link to="/about">About Us</Link>
        <Link to="/jobs">Jobs</Link>
        <Link to="/make-cv">Make CV</Link>
        {user ? (
          <>
            <Link to="/dashboard">Dashboard</Link>
            <button onClick={() => { logout(); nav("/"); }} className="text-red-500">Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register" className="px-3 py-1 bg-indigo-600 text-white rounded">Register</Link>
            <Link to="/member-login" className="text-indigo-600">Member</Link>
          </>
        )}
      </div>
    </nav>
  );
}
