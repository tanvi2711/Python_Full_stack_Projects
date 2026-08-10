import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  ArrowRight,
  BriefcaseBusiness,
  CheckCircle2,
  Eye,
  EyeOff,
  LockKeyhole,
  Mail,
  Phone,
  ShieldCheck,
  UserRound,
} from "lucide-react";
import api, { ensureCsrf } from "../services/api";
import "./Register.css";

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: "",
    email: "",
    phone: "",
    password: "",
    confirmPassword: "",
    role: "candidate",
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    ensureCsrf().catch(() => {});
  }, []);

  const update = (field) => (event) => {
    setForm((current) => ({ ...current, [field]: event.target.value }));
    setMessage("");
  };

  const submit = async (event) => {
    event.preventDefault();
    setMessage("");
    setSuccess(false);

    if (!form.username.trim() || !form.email.trim() || !form.password) {
      setMessage("Username, email and password are required.");
      return;
    }

    if (form.password !== form.confirmPassword) {
      setMessage("Passwords do not match.");
      return;
    }

    try {
      setLoading(true);
      await api.post("/auth/register/", {
        username: form.username.trim(),
        email: form.email.trim().toLowerCase(),
        phone: form.phone.trim(),
        password: form.password,
        role: form.role,
      });

      setSuccess(true);
      setTimeout(() => navigate("/login", { replace: true, state: { registered: true } }), 900);
    } catch (error) {
      const data = error.response?.data;
      const backendMessage = Array.isArray(data?.message)
        ? data.message.join(" ")
        : data?.message;
      setMessage(backendMessage || "Unable to create your account. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="register-page">
      <div className="register-orb register-orb-one" />
      <div className="register-orb register-orb-two" />

      <section className="register-shell">
        <div className="register-brand">
          <div className="register-brand-mark">H</div>
          <div>
            <strong>HireFlow</strong>
            <span>Find. Apply. Grow.</span>
          </div>
        </div>

        <div className="register-grid">
          <aside className="register-story">
            <div className="register-story-icon"><BriefcaseBusiness size={24} /></div>
            <span className="register-eyebrow">START YOUR JOURNEY</span>
            <h1>Create your HireFlow account.</h1>
            <p>
              Build your profile, discover relevant jobs and keep your entire
              application journey organized in one place.
            </p>

            <div className="register-benefits">
              <div><CheckCircle2 size={18} /><span>Personalized job discovery</span></div>
              <div><CheckCircle2 size={18} /><span>Track every application</span></div>
              <div><ShieldCheck size={18} /><span>Secure Django authentication</span></div>
            </div>
          </aside>

          <div className="register-card">
            <div className="register-card-head">
              <span className="register-card-eyebrow">CREATE ACCOUNT</span>
              <h2>Join HireFlow</h2>
              <p>Set up your account in less than a minute.</p>
            </div>

            <form onSubmit={submit} className="register-form">
              <div className="register-row">
                <label>
                  Username
                  <div className="register-input-wrap">
                    <UserRound size={17} />
                    <input
                      value={form.username}
                      onChange={update("username")}
                      placeholder="Choose a username"
                      autoComplete="username"
                    />
                  </div>
                </label>

                <label>
                  Email
                  <div className="register-input-wrap">
                    <Mail size={17} />
                    <input
                      type="email"
                      value={form.email}
                      onChange={update("email")}
                      placeholder="you@example.com"
                      autoComplete="email"
                    />
                  </div>
                </label>
              </div>

              <div className="register-row">
                <label>
                  Phone <span className="optional">Optional</span>
                  <div className="register-input-wrap">
                    <Phone size={17} />
                    <input
                      type="tel"
                      value={form.phone}
                      onChange={update("phone")}
                      placeholder="10-digit phone number"
                      autoComplete="tel"
                    />
                  </div>
                </label>

                <label>
                  Account type
                  <div className="register-input-wrap select-wrap">
                    <BriefcaseBusiness size={17} />
                    <select value={form.role} onChange={update("role")}>
                      <option value="candidate">Candidate</option>
                      <option value="recruiter">Recruiter</option>
                    </select>
                  </div>
                </label>
              </div>

              <div className="register-row">
                <label>
                  Password
                  <div className="register-input-wrap">
                    <LockKeyhole size={17} />
                    <input
                      type={showPassword ? "text" : "password"}
                      value={form.password}
                      onChange={update("password")}
                      placeholder="Create a strong password"
                      autoComplete="new-password"
                    />
                    <button
                      type="button"
                      className="register-password-toggle"
                      onClick={() => setShowPassword((value) => !value)}
                      aria-label="Toggle password visibility"
                    >
                      {showPassword ? <EyeOff size={17} /> : <Eye size={17} />}
                    </button>
                  </div>
                </label>

                <label>
                  Confirm password
                  <div className="register-input-wrap">
                    <LockKeyhole size={17} />
                    <input
                      type={showConfirmPassword ? "text" : "password"}
                      value={form.confirmPassword}
                      onChange={update("confirmPassword")}
                      placeholder="Repeat your password"
                      autoComplete="new-password"
                    />
                    <button
                      type="button"
                      className="register-password-toggle"
                      onClick={() => setShowConfirmPassword((value) => !value)}
                      aria-label="Toggle confirm password visibility"
                    >
                      {showConfirmPassword ? <EyeOff size={17} /> : <Eye size={17} />}
                    </button>
                  </div>
                </label>
              </div>

              {message && <div className="register-message">{message}</div>}
              {success && (
                <div className="register-success">
                  <CheckCircle2 size={17} /> Account created successfully. Redirecting to login…
                </div>
              )}

              <button className="register-submit" disabled={loading || success}>
                {loading ? (
                  <>
                    <span className="register-spinner" /> Creating account…
                  </>
                ) : (
                  <>
                    Create account <ArrowRight size={18} />
                  </>
                )}
              </button>
            </form>

            <div className="register-login-link">
              Already have an account? <Link to="/login">Sign in</Link>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
