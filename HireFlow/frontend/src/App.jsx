import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Jobs from "./pages/Jobs";
import Applications from "./pages/Applications";
import Profile from "./pages/Profile";
import SavedJobs from "./pages/SavedJobs";
import RecruiterDashboard from "./pages/RecruiterDashboard";
import RecruiterJobs from "./pages/RecruiterJobs";
import RecruiterJobForm from "./pages/RecruiterJobForm";
import RecruiterApplicants from "./pages/RecruiterApplicants";
import RecruiterProfile from "./pages/RecruiterProfile";
import "./App.css";

function RoleRoute({ role, children }) {
  const user = JSON.parse(localStorage.getItem("hireflow_user") || "null");
  if (!user) return <Navigate to="/login" replace />;
  if (user.role !== role) {
    return <Navigate to={user.role === "recruiter" ? "/recruiter/dashboard" : "/dashboard"} replace />;
  }
  return children;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route path="/dashboard" element={<RoleRoute role="candidate"><Dashboard /></RoleRoute>} />
        <Route path="/jobs" element={<RoleRoute role="candidate"><Jobs /></RoleRoute>} />
        <Route path="/applications" element={<RoleRoute role="candidate"><Applications /></RoleRoute>} />
        <Route path="/profile" element={<RoleRoute role="candidate"><Profile /></RoleRoute>} />
        <Route path="/saved" element={<RoleRoute role="candidate"><SavedJobs /></RoleRoute>} />

        <Route path="/recruiter/dashboard" element={<RoleRoute role="recruiter"><RecruiterDashboard /></RoleRoute>} />
        <Route path="/recruiter/jobs" element={<RoleRoute role="recruiter"><RecruiterJobs /></RoleRoute>} />
        <Route path="/recruiter/jobs/new" element={<RoleRoute role="recruiter"><RecruiterJobForm /></RoleRoute>} />
        <Route path="/recruiter/jobs/:id/edit" element={<RoleRoute role="recruiter"><RecruiterJobForm /></RoleRoute>} />
        <Route path="/recruiter/jobs/:id/applicants" element={<RoleRoute role="recruiter"><RecruiterApplicants /></RoleRoute>} />
        <Route path="/recruiter/profile" element={<RoleRoute role="recruiter"><RecruiterProfile /></RoleRoute>} />

        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
