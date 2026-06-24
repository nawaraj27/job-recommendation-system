import { create } from "zustand";
import axios from "axios";

const saved = JSON.parse(localStorage.getItem("auth") || "null");

export const useAuth = create((set, get) => ({
  access: saved?.access || null,
  refresh: saved?.refresh || null,
  user: saved?.user || null,

  persist: () => {
    const { access, refresh, user } = get();
    localStorage.setItem("auth", JSON.stringify({ access, refresh, user }));
  },

  login: async (username, password) => {
    const { data } = await axios.post("/api/auth/login/", { username, password });
    set({ access: data.access, refresh: data.refresh, user: data.user });
    get().persist();
    return data.user;
  },

  register: async (payload) => {
    await axios.post("/api/auth/register/", payload);
    return get().login(payload.username, payload.password);
  },

  refreshToken: async () => {
    try {
      const { data } = await axios.post("/api/auth/refresh/", { refresh: get().refresh });
      set({ access: data.access });
      get().persist();
      return true;
    } catch {
      return false;
    }
  },

  logout: () => {
    set({ access: null, refresh: null, user: null });
    localStorage.removeItem("auth");
  },
}));
