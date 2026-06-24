import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import api from "../api/client";

export default function Jobs() {
  const [search, setSearch] = useState("");
  const [location, setLocation] = useState("");
  const { data, isLoading } = useQuery({
    queryKey: ["jobs", search, location],
    queryFn: async () => {
      const params = {};
      if (search) params.search = search;
      if (location) params.location = location;
      return (await api.get("/jobs/", { params })).data;
    },
  });
  const jobs = data?.results || [];

  return (
    <div className="max-w-5xl mx-auto px-6 py-12">
      <div className="flex gap-3 mb-8">
        <input value={search} onChange={(e) => setSearch(e.target.value)}
          placeholder="Search title or skill" className="border rounded px-3 py-2 flex-1" />
        <input value={location} onChange={(e) => setLocation(e.target.value)}
          placeholder="Location" className="border rounded px-3 py-2" />
      </div>
      {isLoading ? <p className="text-gray-400">Loading…</p> : (
        <div className="grid gap-4">
          {jobs.map((j) => (
            <Link key={j.id} to={`/jobs/${j.id}`} className="block p-5 border rounded-lg hover:shadow">
              <h3 className="font-semibold text-lg">{j.title}</h3>
              <p className="text-sm text-gray-500">{j.company_name} · {j.location || "Remote"}</p>
              <p className="text-sm mt-2 line-clamp-2 text-gray-600">{j.description}</p>
            </Link>
          ))}
          {jobs.length === 0 && <p className="text-gray-400">No jobs found.</p>}
        </div>
      )}
    </div>
  );
}
