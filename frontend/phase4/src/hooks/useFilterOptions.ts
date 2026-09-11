import { useQuery } from "@tanstack/react-query";

import { getFilterOptions } from "../services/api";

export function useFilterOptions() {
  return useQuery({
    queryKey: ["filters", "options"],
    queryFn: getFilterOptions,
  });
}
