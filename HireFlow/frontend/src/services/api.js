import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api",
  withCredentials: true,
  headers: { Accept: "application/json" },
});

function getCookie(name) {
  const value = document.cookie
    .split(";")
    .map((item) => item.trim())
    .find((item) => item.startsWith(`${name}=`));
  return value ? decodeURIComponent(value.split("=").slice(1).join("=")) : null;
}

let csrfPromise = null;

export async function ensureCsrf() {
  if (getCookie("csrftoken")) return getCookie("csrftoken");
  if (!csrfPromise) {
    csrfPromise = api.get("/auth/csrf/").finally(() => {
      csrfPromise = null;
    });
  }
  await csrfPromise;
  return getCookie("csrftoken");
}

api.interceptors.request.use(async (config) => {
  const method = (config.method || "get").toLowerCase();
  if (["post", "put", "patch", "delete"].includes(method)) {
    const token = await ensureCsrf();
    if (token) config.headers["X-CSRFToken"] = token;
  }
  return config;
});

export default api;
