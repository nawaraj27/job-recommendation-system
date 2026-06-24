import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import ProtectedRoute from "./components/ProtectedRoute";
import Home from "./pages/Home";
import About from "./pages/About";
import Jobs from "./pages/Jobs";
import JobDetail from "./pages/JobDetail";
import MakeCV from "./pages/MakeCV";
import Login from "./pages/Login";
import Register from "./pages/Register";
import MemberLogin from "./pages/MemberLogin";
import Dashboard from "./pages/Dashboard";
import Analyze from "./pages/Analyze";
import Interview from "./pages/Interview";

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/jobs" element={<Jobs />} />
        <Route path="/jobs/:id" element={<JobDetail />} />
        <Route path="/make-cv" element={<MakeCV />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/member-login" element={<MemberLogin />} />
        <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/analyze" element={<ProtectedRoute><Analyze /></ProtectedRoute>} />
        <Route path="/interview/:id" element={<ProtectedRoute><Interview /></ProtectedRoute>} />
      </Routes>
    </Layout>
  );
}
