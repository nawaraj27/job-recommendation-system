import { useQuery } from "@tanstack/react-query";
import api from "./client";

export function useCmsGroup(group) {
  return useQuery({
    queryKey: ["cms", group],
    queryFn: async () => (await api.get(`/cms/content/group/${group}/`)).data,
  });
}
