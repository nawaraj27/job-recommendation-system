import axios from "axios";
import { useAuth } from "../store/auth";

const api = axios.create({ baseURL: "/api" });

api.interceptors.request.use((config) => {
  const token = useAuth.getState().access;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (r) => r,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      const ok = await useAuth.getState().refreshToken();
      if (ok) {
        original.headers.Authorization = `Bearer ${useAuth.getState().access}`;
        return api(original);
      }
      useAuth.getState().logout();
    }
    return Promise.reject(error);
  }
);

export default api;
