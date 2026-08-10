import { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import {
  Bell,
  BriefcaseBusiness,
  Building2,
  ChevronRight,
  LayoutDashboard,
  LogOut,
  Menu,
  Plus,
  Users,
  X,
} from "lucide-react";
import api from "../services/api";
import "./RecruiterLayout.css";

export default function RecruiterLayout({ children, title, subtitle }) {
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const user = JSON.parse(localStorage.getItem("hireflow_user") || "null");
  const name = user?.username || "Recruiter";
  const initials = name.slice(0, 1).toUpperCase();

  const logout = async () => {
    try {
      await api.post("/auth/logout/");
    } catch {
      // The local session is still cleared even if the server is unreachable.
    } finally {
      localStorage.removeItem("hireflow_user");
      navigate("/login", { replace: true });
    }
  };

  const close = () => setOpen(false);

  return (
    <div className="recruiter-app">
      {open && <div className="recruiter-overlay" onClick={close} />}
      <aside className={`recruiter-sidebar ${open ? "open" : ""}`}>
        <div className="recruiter-brand">
          <div className="recruiter-logo">H</div>
          <div>
            <strong>HireFlow</strong>
            <span>Recruiter workspace</span>
          </div>
          <button className="mobile-close" onClick={close} aria-label="Close menu"><X size={18} /></button>
        </div>

        <div className="recruiter-nav-label">WORKSPACE</div>
        <nav className="recruiter-nav">
          <NavLink end to="/recruiter/dashboard" onClick={close}>
            <LayoutDashboard size={18} /> Dashboard
          </NavLink>
          <NavLink end to="/recruiter/jobs" onClick={close}>
            <BriefcaseBusiness size={18} /> My Jobs
          </NavLink>
          <NavLink to="/recruiter/jobs/new" onClick={close}>
            <Plus size={18} /> Post a Job
          </NavLink>
          <NavLink to="/recruiter/profile" onClick={close}>
            <Building2 size={18} /> Company Profile
          </NavLink>
        </nav>

        <div className="recruiter-sidebar-bottom">
          <div className="recruiter-account">
            <div className="recruiter-avatar">{initials}</div>
            <div className="recruiter-account-text">
              <strong>{name}</strong>
              <span>Recruiter</span>
            </div>
          </div>
          <button className="recruiter-logout" onClick={logout}><LogOut size={17} /> Sign out</button>
        </div>
      </aside>

      <main className="recruiter-main">
        <header className="recruiter-topbar">
          <button className="mobile-menu" onClick={() => setOpen(true)} aria-label="Open menu"><Menu size={22} /></button>
          <div>
            <div className="recruiter-breadcrumb">RECRUITER / {title?.toUpperCase()}</div>
            <h1>{title}</h1>
            {subtitle && <p>{subtitle}</p>}
          </div>
          <div className="recruiter-top-actions">
            <button className="icon-button" title="Notifications"><Bell size={18} /><span className="notification-dot" /></button>
            <button className="top-profile" onClick={() => navigate("/recruiter/profile")}>
              <div className="recruiter-avatar small">{initials}</div>
              <span>{name}</span>
              <ChevronRight size={15} />
            </button>
          </div>
        </header>
        <section className="recruiter-content">{children}</section>
      </main>
    </div>
  );
}
