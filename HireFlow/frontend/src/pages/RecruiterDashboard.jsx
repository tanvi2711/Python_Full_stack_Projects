import { useEffect, useState } from "react";
import { ArrowUpRight, BriefcaseBusiness, CheckCircle2, Clock3, Plus, Users, UserRoundCheck } from "lucide-react";
import { Link } from "react-router-dom";
import api from "../services/api";
import RecruiterLayout from "./RecruiterLayout";
import "./RecruiterDashboard.css";

const fmtDate = (value) => value ? new Date(value).toLocaleDateString(undefined,{day:"2-digit",month:"short",year:"numeric"}) : "—";

export default function RecruiterDashboard(){
  const [data,setData]=useState(null); const [loading,setLoading]=useState(true); const [error,setError]=useState("");
  useEffect(()=>{api.get("/recruiter/dashboard/").then(r=>setData(r.data)).catch(e=>setError(e.response?.data?.message||"Unable to load recruiter dashboard.")).finally(()=>setLoading(false));},[]);
  const s=data?.stats||{};
  return <RecruiterLayout title="Recruiter Dashboard" subtitle="Manage your openings and move candidates through the hiring pipeline.">
    {loading ? <div className="recruiter-loading">Loading your hiring workspace…</div> : error ? <div className="recruiter-error">{error}</div> : <>
      <div className="recruiter-hero">
        <div><span className="hero-eyebrow">HIRING WORKSPACE</span><h2>Build your next great team.</h2><p>Post roles, review applicants and keep every hiring decision in one place.</p></div>
        <Link className="primary-cta" to="/recruiter/jobs/new"><Plus size={17}/> Post a new job</Link>
      </div>
      <div className="recruiter-stat-grid">
        <Stat icon={<BriefcaseBusiness/>} label="Total jobs" value={s.total_jobs||0} tone="purple" />
        <Stat icon={<CheckCircle2/>} label="Open jobs" value={s.open_jobs||0} tone="green" />
        <Stat icon={<Users/>} label="Applications" value={s.total_applications||0} tone="blue" />
        <Stat icon={<UserRoundCheck/>} label="Shortlisted" value={s.shortlisted||0} tone="orange" />
      </div>
      <div className="recruiter-dashboard-grid">
        <section className="panel"><div className="panel-head"><div><h3>Recent job postings</h3><p>Your latest openings and applicant volume.</p></div><Link to="/recruiter/jobs">View all <ArrowUpRight size={14}/></Link></div>
          {data?.recent_jobs?.length ? <div className="recent-jobs">{data.recent_jobs.map(job=><Link className="recent-job" key={job.id} to={`/recruiter/jobs/${job.id}/applicants`}><div className="recent-job-icon"><BriefcaseBusiness size={18}/></div><div className="recent-job-main"><strong>{job.title}</strong><span>{job.location} · {job.job_type.replace("-"," ")}</span></div><div className="recent-job-meta"><b>{job.applicant_count}</b><span>applicants</span></div><Status status={job.status}/></Link>)}</div> : <Empty title="No jobs yet" text="Post your first opening to start receiving applications."/>}
        </section>
        <aside className="panel hiring-panel"><div className="panel-head"><div><h3>Hiring snapshot</h3><p>Pipeline at a glance.</p></div><Clock3 size={18}/></div><div className="snapshot-row"><span>Open positions</span><strong>{s.open_jobs||0}</strong></div><div className="snapshot-row"><span>Closed positions</span><strong>{s.closed_jobs||0}</strong></div><div className="snapshot-row"><span>Shortlisted</span><strong>{s.shortlisted||0}</strong></div><div className="snapshot-row"><span>Hired</span><strong>{s.hired||0}</strong></div><Link className="secondary-cta" to="/recruiter/jobs"><Users size={16}/> Review applicants</Link></aside>
      </div>
    </>}
  </RecruiterLayout>
}
function Stat({icon,label,value,tone}){return <div className="recruiter-stat"><div className={`stat-icon ${tone}`}>{icon}</div><div><span>{label}</span><strong>{value}</strong></div></div>}
function Status({status}){return <span className={`job-status ${status}`}>{status}</span>}
function Empty({title,text}){return <div className="empty-state"><BriefcaseBusiness size={24}/><strong>{title}</strong><p>{text}</p></div>}
