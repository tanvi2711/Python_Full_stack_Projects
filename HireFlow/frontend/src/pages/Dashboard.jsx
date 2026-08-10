import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Activity, ArrowRight, Bell, Bookmark, BriefcaseBusiness, CheckCircle2, ChevronRight, Clock3, FileText, Heart, Home, LogOut, Menu, Search, Settings, ShieldCheck, Sparkles, UserRound, X } from "lucide-react";
import api from "../services/api";
import "./Dashboard.css";

const savedKey="hireflow_saved_jobs";
const fmtSalary=(min,max)=>min&&max?`₹${Number(min).toLocaleString("en-IN")} - ₹${Number(max).toLocaleString("en-IN")}`:"Salary not disclosed";
const timeAgo=(date)=>{if(!date)return "Recently";const d=new Date(date),diff=Math.max(0,Date.now()-d.getTime()),m=Math.floor(diff/60000);if(m<60)return `${m||1} min ago`;const h=Math.floor(m/60);if(h<24)return `${h}h ago`;const days=Math.floor(h/24);return `${days}d ago`};

export default function Dashboard(){
 const navigate=useNavigate(); const [user,setUser]=useState(null); const [profile,setProfile]=useState(null); const [jobs,setJobs]=useState([]); const [applications,setApplications]=useState([]); const [saved,setSaved]=useState(()=>JSON.parse(localStorage.getItem(savedKey)||"[]")); const [loading,setLoading]=useState(true); const [error,setError]=useState(""); const [mobileOpen,setMobileOpen]=useState(false); const [search,setSearch]=useState("");
 useEffect(()=>{localStorage.setItem(savedKey,JSON.stringify(saved))},[saved]);
 useEffect(()=>{(async()=>{try{setLoading(true);const [me,j,p]=await Promise.all([api.get("/auth/me/"),api.get("/jobs/list/?page=1&page_size=6"),api.get("/profile/")]);setUser(me.data.user);setJobs(j.data.jobs||[]);setProfile(p.data.profile||null);try{const a=await api.get("/applications/mine/");setApplications(a.data.applications||[])}catch{setApplications([])}}catch(e){if(e.response?.status===401){navigate("/login",{replace:true});return}setError(e.response?.data?.message||"Could not load your dashboard.")}finally{setLoading(false)}})()},[navigate]);
 const counts=useMemo(()=>({total:applications.length,review:applications.filter(a=>a.status==="applied").length,shortlisted:applications.filter(a=>a.status==="shortlisted").length,saved:saved.length}),[applications,saved]);
 const profileStrength=useMemo(()=>{if(!profile)return 0;const fields=[profile.full_name,profile.location,profile.education,profile.experience_years!==undefined,profile.bio];return Math.round(fields.filter(Boolean).length/fields.length*100)},[profile]);
 const filteredJobs=useMemo(()=>{const q=search.trim().toLowerCase();return q?jobs.filter(j=>`${j.title} ${j.posted_by} ${j.location} ${(j.skills||[]).map(s=>s.name).join(" ")}`.toLowerCase().includes(q)):jobs},[jobs,search]);
 const toggleSave=id=>setSaved(s=>s.includes(id)?s.filter(x=>x!==id):[...s,id]);
 const logout=async()=>{try{await api.post("/auth/logout/")}catch{}navigate("/login",{replace:true})};
 if(loading)return <div className="app-loading"><div><div className="spinner"/><p>Loading your HireFlow dashboard...</p></div></div>;
 const name=user?.username||"there", initials=name.slice(0,1).toUpperCase();
 return <div className="hf-app">
   {mobileOpen&&<div className="mobile-backdrop" onClick={()=>{setMobileOpen(false);navigate("/saved")}}/>} 
   <aside className={`hf-sidebar ${mobileOpen?"open":""}`}>
    <div className="sidebar-top"><div className="hf-brand"><div className="hf-logo">H</div><div><strong>HireFlow</strong><span>Find. Apply. Grow.</span></div></div><button className="sidebar-close" onClick={()=>setMobileOpen(false)}><X size={20}/></button></div>
    <div className="hf-sidebar-scroll">
      <div className="sidebar-section-title">MAIN MENU</div><nav className="hf-nav">
       <NavItem icon={<Home/>} label="Dashboard" active onClick={()=>{setMobileOpen(false);navigate("/dashboard")}}/>
       <NavItem icon={<Search/>} label="Find Jobs" onClick={()=>{setMobileOpen(false);navigate("/jobs")}}/>
       <NavItem icon={<FileText/>} label="Applications" count={counts.total} onClick={()=>{setMobileOpen(false);navigate("/applications")}}/>
       <NavItem icon={<Bookmark/>} label="Saved Jobs" count={counts.saved} onClick={()=>setMobileOpen(false)}/>
      </nav>
      <div className="sidebar-section-title account-title">ACCOUNT</div><nav className="hf-nav">
       <NavItem icon={<UserRound/>} label="My Profile" onClick={()=>{setMobileOpen(false);navigate("/profile")}}/>
       <NavItem icon={<Settings/>} label="Settings" disabled onClick={()=>{}}/>
      </nav>
      <div className="career-card"><div className="career-icon"><Sparkles size={18}/></div><h3>Keep your profile ready</h3><p>A complete profile helps recruiters understand your strengths faster.</p><button onClick={()=>navigate("/profile")}>Complete Profile <ArrowRight size={15}/></button></div>
      <button className="logout-button" onClick={logout}><LogOut size={18}/><span>Logout</span></button>
    </div>
   </aside>
   <main className="hf-main">
    <header className="topbar"><button className="mobile-menu" onClick={()=>setMobileOpen(true)}><Menu size={22}/></button><div className="search-box"><Search size={18}/><input value={search} onChange={e=>setSearch(e.target.value)} placeholder="Search jobs, companies, skills..."/><span className="shortcut">⌘ K</span></div><div className="top-actions"><button className="top-action"><Sparkles size={18}/></button><button className="top-action"><Bell size={18}/><span className="notification-dot">{applications.filter(a=>a.status==="shortlisted").length}</span></button><button className="user-menu" onClick={()=>navigate("/profile")}><div className="avatar">{initials}</div><div className="user-info"><strong>{name}</strong><span>{user?.role=== "recruiter"?"Recruiter":"Job Seeker"}</span></div><ChevronRight size={18}/></button></div></header>
    <div className="dashboard-content">
      {error&&<div className="dashboard-alert">{error}</div>}
      <section className="hero"><div className="hero-content"><div className="eyebrow">YOUR CAREER DASHBOARD</div><h1>Good evening, <span>{name}</span> <span className="wave">👋</span></h1><p>Discover opportunities that match your skills, experience and career goals.</p><button className="primary-button" onClick={()=>navigate("/jobs")}><Search size={17}/>Find New Jobs<ArrowRight size={17}/></button></div><div className="hero-decoration"><div className="hero-glow"/><div className="growth-card"><Activity size={58}/></div><div className="matched-pill"><CheckCircle2 size={14}/> Profile matched {profileStrength}%</div><i className="floating-dot dot-one"/><i className="floating-dot dot-two"/><i className="floating-dot dot-three"/></div></section>
      <section className="stats-grid"><StatCard icon={<FileText/>} cls="blue" title="Applications" number={counts.total} desc="Applications submitted"/><StatCard icon={<Clock3/>} cls="cyan" title="In Review" number={counts.review} desc="Waiting for recruiter response"/><StatCard icon={<CheckCircle2/>} cls="green" title="Shortlisted" number={counts.shortlisted} desc="You made the shortlist"/><StatCard icon={<Bookmark/>} cls="slate" title="Saved Jobs" number={counts.saved} desc="Saved on this device"/></section>
      <div className="dashboard-grid"><section className="jobs-section"><div className="section-heading"><div><span className="section-kicker">MATCHED OPPORTUNITIES</span><h2>Recommended for you</h2><p>Latest open roles from your HireFlow marketplace.</p></div><button className="view-all" onClick={()=>navigate("/jobs")}>View all jobs <ArrowRight size={15}/></button></div><div className="jobs-list">{filteredJobs.slice(0,3).map((job,i)=><JobCard key={job.id} job={job} index={i} saved={saved.includes(job.id)} onSave={()=>toggleSave(job.id)} onApply={()=>navigate(`/jobs?apply=${job.id}`)}/>)}{!filteredJobs.length&&<div className="empty-card"><BriefcaseBusiness size={28}/><h3>No matching jobs</h3><p>Try a different search or browse all open positions.</p><button onClick={()=>{setSearch("");navigate("/jobs")}}>Browse jobs</button></div>}</div></section>
      <aside className="right-column"><div className="profile-card"><div className="profile-top"><div className="profile-avatar">{initials}</div><div><h3>{profile?.full_name||name}</h3><p>{profile?.education||"Complete your profile"}</p></div></div><div className="strength-header"><span>Profile Strength</span><strong>{profileStrength}%</strong></div><div className="progress-track"><div className="progress-value" style={{width:`${profileStrength}%`}}/></div><button className="profile-button" onClick={()=>navigate("/profile")}>{profileStrength===100?"View Profile":"Complete Profile"}<ArrowRight size={15}/></button></div>
      <div className="activity-card"><div className="activity-heading"><div><span className="section-kicker">YOUR JOURNEY</span><h2>Recent Activity</h2></div></div>{applications.slice(0,4).map(a=><div className="activity-item" key={a.id}><div className={`activity-icon ${a.status}`}><Activity size={16}/></div><div className="activity-content"><strong>{a.status.charAt(0).toUpperCase()+a.status.slice(1)}</strong><span>{a.job_title}</span><small>{timeAgo(a.applied_at)}</small></div></div>)}{!applications.length&&<div className="activity-empty">Your application activity will appear here.</div>}</div></aside></div>
    </div>
   </main>
 </div>;
}

function NavItem({icon,label,active,count,onClick,disabled}){return <button className={`hf-nav-item ${active?"active":""}`} disabled={disabled} onClick={onClick}>{icon}<span>{label}</span>{count>0&&<b>{count}</b>}</button>}
function StatCard({icon,cls,title,number,desc}){return <div className="stat-card"><div className={`stat-icon ${cls}`}>{icon}</div><span className="stat-label">LIVE</span><div className="stat-title">{title}</div><div className="stat-number">{String(number).padStart(2,"0")}</div><div className="stat-description">{desc}</div></div>}
function JobCard({job,index,saved,onSave,onApply}){return <article className={`job-card ${index===0?"featured-job":""}`}><div className="company-logo">{job.title?.slice(0,1).toUpperCase()}</div><div className="job-info"><div className="job-title-row"><h3>{job.title}</h3><ShieldCheck size={15}/></div><p className="company-name">{job.posted_by}</p><div className="job-meta"><span>⌖ {job.location}</span><span>◷ {job.job_type}</span><span>{fmtSalary(job.salary_min,job.salary_max)}</span></div><div className="job-tags">{(job.skills||[]).slice(0,5).map(s=><span key={s.id}>{s.name}</span>)}</div></div><div className="job-actions"><button className={`save-job ${saved?"saved":""}`} onClick={onSave}><Heart size={15} fill={saved?"currentColor":"none"}/>{saved?"Saved":"Save"}</button><button className="apply-button" onClick={onApply}>Apply Now <ArrowRight size={15}/></button><small>Posted {timeAgo(job.created_at)}</small></div></article>}
