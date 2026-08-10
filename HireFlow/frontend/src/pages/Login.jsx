import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { ArrowRight, BriefcaseBusiness, Eye, EyeOff, LockKeyhole, Mail, ShieldCheck, Sparkles, UserRound } from "lucide-react";
import api, { ensureCsrf } from "../services/api";
import "./Login.css";

export default function Login() {
  const navigate = useNavigate();
  const location = useLocation();
  const [username,setUsername]=useState("");
  const [password,setPassword]=useState("");
  const [showPassword,setShowPassword]=useState(false);
  const [loading,setLoading]=useState(false);
  const [message,setMessage]=useState(location.state?.registered ? "Account created successfully. Please sign in." : "");

  useEffect(()=>{ ensureCsrf().catch(()=>{}); },[]);

  const submit=async(e)=>{
    e.preventDefault(); setMessage("");
    if(!username.trim() || !password){setMessage("Enter your username and password.");return;}
    try{
      setLoading(true);
      const response = await api.post("/auth/login/",{username:username.trim(),password});
      const user = response.data.user;
      localStorage.setItem("hireflow_user", JSON.stringify(user));
      navigate(user.role === "recruiter" ? "/recruiter/dashboard" : "/dashboard",{replace:true});
    }catch(error){
      setMessage(error.response?.data?.message || "Unable to sign in. Check your credentials.");
    }finally{setLoading(false);}
  };

  return <main className="login-page">
    <div className="login-orb orb-one"/><div className="login-orb orb-two"/>
    <section className="login-shell">
      <div className="login-brand"><div className="brand-mark">H</div><div><strong>HireFlow</strong><span>Find. Apply. Grow.</span></div></div>
      <div className="login-grid">
        <div className="login-story">
          <span className="story-badge"><Sparkles size={15}/> Smart job discovery</span>
          <h1>Build your next career move with confidence.</h1>
          <p>Discover relevant opportunities, manage applications and keep your professional profile ready for recruiters.</p>
          <div className="story-points">
            <div><ShieldCheck size={18}/><span>Secure Django authentication</span></div>
            <div><BriefcaseBusiness size={18}/><span>Real-time job listings</span></div>
            <div><ArrowRight size={18}/><span>Simple, recruiter-friendly workflow</span></div>
          </div>
        </div>
        <div className="login-card">
          <div className="login-card-head"><span className="eyebrow">WELCOME BACK</span><h2>Sign in to HireFlow</h2><p>Use your HireFlow account to continue.</p></div>
          <form onSubmit={submit} className="login-form">
            <label>Username<div className="input-wrap"><UserRound size={18}/><input value={username} onChange={e=>setUsername(e.target.value)} placeholder="Enter username" autoComplete="username"/></div></label>
            <label>Password<div className="input-wrap"><LockKeyhole size={18}/><input type={showPassword?"text":"password"} value={password} onChange={e=>setPassword(e.target.value)} placeholder="Enter password" autoComplete="current-password"/><button type="button" className="password-toggle" onClick={()=>setShowPassword(v=>!v)} aria-label="Toggle password">{showPassword?<EyeOff size={17}/>:<Eye size={17}/>}</button></div></label>
            {message && <div className={`login-message ${location.state?.registered ? "login-success" : ""}`}>{message}</div>}
            <button className="login-submit" disabled={loading}>{loading?<span className="button-spinner"/>:<><span>Sign in</span><ArrowRight size={18}/></>}{loading&&<span>Signing in...</span>}</button>
          </form>
          <div className="login-register">Don’t have an account? <Link to="/register">Create one</Link></div>
          <div className="login-footer"><Mail size={15}/> Your session is protected by Django authentication.</div>
        </div>
      </div>
    </section>
  </main>;
}
